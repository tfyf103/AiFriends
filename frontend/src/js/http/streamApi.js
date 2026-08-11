/*
 * AiFriends 的“流式 HTTP 请求”封装。
 *
 * 为什么不能直接复用普通 axios 请求？
 * ----------------------------------
 * 普通 axios 更适合“请求一次 -> 等后端全部算完 -> 一次性返回 JSON”。
 * 但聊天接口希望模型生成一个片段，浏览器就立刻显示一个片段，因此这里使用
 * Server-Sent Events（SSE）持续接收后端发送的 data: ... 消息。
 *
 * 这个文件主要解决 4 件事：
 * 1. 自动携带 JWT access token；
 * 2. 建立并持续监听 SSE 连接；
 * 3. access token 过期后刷新 token 并重新建立流；
 * 4. 把后端的 SSE 文本解析成普通 JavaScript 对象交给页面组件。
 *
 * 建议零基础同学先看懂普通 api.js，再阅读本文件。
 */

import { fetchEventSource } from '@microsoft/fetch-event-source';
import { useUserStore } from "@/stores/user.js";
import api from "./api.js";
import CONFIG_API from "@/js/config/config.js";

// 开发环境一般是 http://127.0.0.1:8000。
// 将地址集中到 config.js，可以避免每个组件都写死后端地址。
const BASE_URL = CONFIG_API.HTTP_URL

/**
 * 通用 SSE 请求工具。
 *
 * 调用示例：
 * await streamApi('/api/friend/message/chat/', {
 *   body: { friend_id: 1, message: '你好' },
 *   onmessage(data, isDone) { ... }
 * })
 *
 * @param {string} url Django API 路径
 * @param {object} options 请求配置：method、body、headers、onmessage、onerror 等
 */
export default async function streamApi(url, options = {}) {
    // Pinia 中保存当前登录用户的 access token。
    const userStore = useUserStore();

    /**
     * 真正建立 SSE 连接的内部函数。
     *
     * 单独封装成 startFetch() 的原因是：token 刷新成功后，我们需要“重新连接一次”。
     * 如果所有代码都直接写在 streamApi() 里，重试逻辑会更难读。
     */
    const startFetch = async () => {
        return await fetchEventSource(BASE_URL + url, {
            method: options.method || 'POST',
            headers: {
                // 聊天接口发送 JSON，所以告诉 Django 请求体的格式。
                'Content-Type': 'application/json',

                // DRF SimpleJWT 默认读取：Authorization: Bearer <access_token>
                'Authorization': `Bearer ${userStore.accessToken}`,

                // 调用者可以继续补充自己的请求头。
                ...options.headers,
            },

            // fetch 的 body 需要字符串，因此把普通 JS 对象转成 JSON。
            body: JSON.stringify(options.body || {}),

            // 默认情况下，某些 SSE 客户端在页面进入后台后可能主动关闭连接。
            // AI 回复可能持续数秒，因此这里允许页面隐藏时继续接收数据。
            openWhenHidden: true,

            /**
             * SSE 连接刚建立时触发。
             * 此时还没有开始处理一条条 data 消息，适合先检查 HTTP 状态码和响应类型。
             */
            async onopen(response) {
                // access token 过期时，Django REST Framework 会返回 401。
                if (response.status === 401) {
                    try {
                        // 这里复用 api.js 的刷新 token 逻辑。
                        // 刷新成功后 Pinia 中的 accessToken 会被更新。
                        await api.post('/api/user/account/refresh_token/', {});

                        // 当前 SSE 请求已经带着旧 token 发出，无法在原连接上“换 token”。
                        // 所以故意抛出一个可识别的错误，让 onerror 重新 startFetch()。
                        throw new Error("TOKEN_REFRESHED");
                    } catch (err) {
                        // refresh token 也失效时，不再无限重试，把错误交给上层处理。
                        throw err;
                    }
                }

                // 一个正常的聊天流必须同时满足：HTTP 成功 + Content-Type 是 text/event-stream。
                // 这能尽早发现 Django 500、404 或返回普通 JSON 错误页等情况。
                if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `请求失败: ${response.status}`);
                }
            },

            /**
             * 每收到一条 SSE 消息就调用一次。
             *
             * Django 端大致会发送：
             * data: {"content":"你"}\n\n
             * data: {"audio":"base64..."}\n\n
             * data: [DONE]\n\n
             */
            onmessage(msg) {
                // [DONE] 是我们自己定义的“流结束标记”，不是 JSON。
                if (msg.data === '[DONE]') {
                    if (options.onmessage) options.onmessage('', true);
                    return
                }

                try {
                    // 普通消息则解析成 { content: ... } 或 { audio: ... }。
                    const json = JSON.parse(msg.data);
                    if (options.onmessage) options.onmessage(json, false);
                } catch (e) {
                    console.error("流解析失败:", e);
                }
            },

            /**
             * 网络错误、协议错误或我们主动抛出的 TOKEN_REFRESHED 都会来到这里。
             */
            onerror(err) {
                // token 已刷新：使用新 token 重新建立 SSE 请求。
                if (err.message === "TOKEN_REFRESHED") {
                    return startFetch();
                }

                // 其他错误交给调用 streamApi() 的页面组件决定如何展示。
                if (options.onerror) {
                    options.onerror(err);
                }

                // 继续向上抛出，阻止 fetch-event-source 对未知错误无限自动重试。
                throw err;
            },

            onclose: options.onclose,
        });
    };

    return await startFetch();
}
