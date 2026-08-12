<script setup>
/*
 * 聊天链路的前端起点：Vue → SSE → Django → LangGraph/Mock → content/audio。
 *
 * 第四轮新增了 AbortController。以前“停止”只是 processId++ 后忽略迟到数据，
 * 服务器请求仍可能继续生成；现在会真正关闭浏览器的 SSE 连接，并由后端的
 * cancel_event 尽快停止后台 LLM/TTS 生产。
 */

import SendIcon from '@/components/character/icons/SendIcon.vue'
import MicIcon from '@/components/character/icons/MicIcon.vue'
import { defineAsyncComponent, onUnmounted, ref, useTemplateRef } from 'vue'
import streamApi from '@/js/http/streamApi.js'

// VAD/ONNX is one of the heaviest browser dependencies. Do not make every homepage
// visitor download it: fetch the microphone implementation only after voice mode is
// actually opened.
const Microphone = defineAsyncComponent(
  () => import('@/components/character/chat_field/input_field/Microphone.vue'),
)

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
const showMic = ref(false)

let processId = 0
let activeController = null

let mediaSource = null
let sourceBuffer = null
let audioPlayer = new Audio()
let audioQueue = []
let isUpdating = false

const initAudioStream = () => {
  stopAudio()
  mediaSource = new MediaSource()
  audioPlayer.src = URL.createObjectURL(mediaSource)

  mediaSource.addEventListener('sourceopen', () => {
    try {
      sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg')
      sourceBuffer.addEventListener('updateend', () => {
        isUpdating = false
        processQueue()
      })
    } catch (error) {
      console.error('MSE AddSourceBuffer Error:', error)
    }
  })

  audioPlayer.play().catch(() => {
    console.info('浏览器等待用户交互后才能播放音频')
  })
}

const processQueue = () => {
  if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) return

  isUpdating = true
  const chunk = audioQueue.shift()
  try {
    sourceBuffer.appendBuffer(chunk)
  } catch (error) {
    console.error('SourceBuffer Append Error:', error)
    isUpdating = false
  }
}

const stopAudio = () => {
  audioPlayer.pause()
  audioQueue = []
  isUpdating = false

  if (mediaSource?.readyState === 'open') {
    try {
      mediaSource.endOfStream()
    } catch {
      // 页面快速关闭时 MediaSource 可能已经切换状态。
    }
  }
  mediaSource = null
  sourceBuffer = null

  if (audioPlayer.src) {
    URL.revokeObjectURL(audioPlayer.src)
    audioPlayer.src = ''
  }
}

const handleAudioChunk = (base64Data) => {
  try {
    const binaryString = atob(base64Data)
    const bytes = new Uint8Array(binaryString.length)
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i)
    }
    audioQueue.push(bytes)
    processQueue()
  } catch (error) {
    console.error('Base64 Decode Error:', error)
  }
}

function abortActiveStream() {
  if (activeController) {
    activeController.abort()
    activeController = null
  }
}

onUnmounted(() => {
  abortActiveStream()
  stopAudio()
})

function focus() {
  inputRef.value?.focus()
}

async function handleSend(event, audioMessage) {
  const content = (audioMessage || message.value).trim()
  if (!content) return

  abortActiveStream()
  activeController = new AbortController()

  initAudioStream()
  const curId = ++processId
  message.value = ''

  emit('pushBackMessage', {
    role: 'user',
    content,
    id: crypto.randomUUID(),
  })
  emit('pushBackMessage', {
    role: 'ai',
    content: '',
    id: crypto.randomUUID(),
  })

  try {
    await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      signal: activeController.signal,

      onmessage(data, isDone) {
        if (curId !== processId) return

        if (data.content) emit('addToLastMessage', data.content)
        if (data.audio) handleAudioChunk(data.audio)
        if (data.error) console.error('AI 流错误:', data.error)

        if (isDone) {
          activeController = null
        }
      },

      onerror(error) {
        console.error('聊天流请求失败:', error)
      },
    })
  } catch (error) {
    if (error?.name !== 'AbortError') {
      console.error('发送消息失败:', error)
    }
  } finally {
    if (curId === processId) activeController = null
  }
}

function close() {
  ++processId
  abortActiveStream()
  showMic.value = false
  stopAudio()
}

function handleStop() {
  ++processId
  abortActiveStream()
  stopAudio()
}

defineExpose({ focus, close })
</script>

<template>
  <form
    v-if="!showMic"
    @submit.prevent="handleSend"
    class="absolute bottom-4 left-2 h-12 w-86 flex items-center"
  >
    <input
      ref="input-ref"
      v-model="message"
      class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
      type="text"
      placeholder="文本输入..."
    >

    <button
      type="submit"
      aria-label="发送消息"
      class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer"
    >
      <SendIcon />
    </button>

    <button
      type="button"
      aria-label="切换语音输入"
      @click="showMic = true"
      class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer"
    >
      <MicIcon />
    </button>
  </form>

  <Microphone
    v-else
    @close="showMic = false"
    @send="handleSend"
    @stop="handleStop"
  />
</template>

<style scoped>
</style>
