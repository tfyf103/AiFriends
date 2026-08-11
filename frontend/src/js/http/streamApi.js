/*
 * SSE request helper used by chat.
 *
 * It shares the exact same refreshAccessToken() function as Axios, so a successful
 * refresh always updates Pinia before the stream reconnects. It also accepts an
 * AbortSignal so the Stop button can close the actual HTTP stream instead of only
 * hiding late UI chunks.
 */

import { fetchEventSource } from '@microsoft/fetch-event-source'
import { useUserStore } from '@/stores/user.js'
import CONFIG_API from '@/js/config/config.js'
import { refreshAccessToken } from '@/js/http/authRefresh.js'

const BASE_URL = CONFIG_API.HTTP_URL

class TokenRefreshedError extends Error {
  constructor() {
    super('TOKEN_REFRESHED')
    this.name = 'TokenRefreshedError'
  }
}

export default async function streamApi(url, options = {}) {
  const userStore = useUserStore()

  const startFetch = async () => {
    try {
      return await fetchEventSource(BASE_URL + url, {
        method: options.method || 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(userStore.accessToken
            ? { Authorization: `Bearer ${userStore.accessToken}` }
            : {}),
          ...options.headers,
        },
        body: JSON.stringify(options.body || {}),
        openWhenHidden: true,
        signal: options.signal,

        async onopen(response) {
          if (response.status === 401) {
            await refreshAccessToken()
            // Reject this old connection. The outer catch below starts a brand-new
            // request whose headers are rebuilt from the new Pinia access token.
            throw new TokenRefreshedError()
          }

          if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
            const errorData = await response.json().catch(() => ({}))
            throw new Error(errorData.detail || errorData.result || `请求失败: ${response.status}`)
          }
        },

        onmessage(msg) {
          if (msg.data === '[DONE]') {
            options.onmessage?.('', true)
            return
          }

          try {
            options.onmessage?.(JSON.parse(msg.data), false)
          } catch (error) {
            console.error('流解析失败:', error)
          }
        },

        onerror(error) {
          // Throwing makes fetchEventSource reject instead of silently retrying with
          // stale request options. The outer catch decides whether reconnect is safe.
          throw error
        },

        onclose: options.onclose,
      })
    } catch (error) {
      if (error instanceof TokenRefreshedError) {
        return startFetch()
      }
      if (error?.name === 'AbortError') {
        return
      }
      options.onerror?.(error)
      throw error
    }
  }

  return startFetch()
}
