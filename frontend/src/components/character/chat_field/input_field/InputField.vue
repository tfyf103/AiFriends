<script setup>
/*
 * 这个组件是“聊天链路”的前端起点。
 *
 * 用户在这里输入文字（或由麦克风识别出文字），点击发送后会发生：
 *
 * InputField.vue
 *   -> streamApi.js 建立 SSE 请求
 *   -> Django MessageChatView
 *   -> LangGraph / LLM
 *   -> 后端不断返回 content 和 audio
 *   -> 本组件把文字追加到消息气泡、把音频片段连续播放
 *
 * 对零基础同学来说，这个组件值得重点学习 4 个知识：
 * 1. Vue 的 props / emits / ref；
 * 2. 表单事件和 v-model；
 * 3. SSE 流式消息如何实时更新页面；
 * 4. MediaSource 如何连续播放后端分片返回的 MP3。
 */

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {onUnmounted, ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

// 父组件把当前好友 id 传进来。
// 后端依靠 friend_id 判断“正在和哪个 AI 角色聊天”。
const props = defineProps(['friendId'])

// 子组件不直接维护完整聊天列表，而是通知父组件：
// pushBackMessage：新增一条消息；
// addToLastMessage：把模型新生成的 token/文本片段追加到最后一条 AI 消息。
const emit = defineEmits(['pushBackMessage','addToLastMessage'])

// useTemplateRef 对应模板里的 ref="input-ref"，用于主动让输入框获取焦点。
const inputRef = useTemplateRef('input-ref')

// ref() 创建响应式变量。message 变化后，模板中的输入框会同步变化。
const message = ref('')

// processId 用来标记“当前这一轮回复”。
// 当用户关闭聊天或主动停止时会自增，让旧请求后续到达的数据失效。
let processId = 0

// false：显示文字输入框；true：切换到麦克风组件。
const showMic = ref(false)

/* --------------------------------------------------------------------------
 * 流式音频播放
 * --------------------------------------------------------------------------
 *
 * 后端不是等整段 TTS 音频生成完再返回，而是一边生成一边通过 SSE 返回 Base64 音频块。
 * 浏览器因此需要一个“音频队列”：收到一块 -> 解码 -> 放进队列 -> 按顺序写入播放器。
 */
let mediaSource = null;
let sourceBuffer = null;
let audioPlayer = new Audio(); // 浏览器原生 Audio 播放器
let audioQueue = [];           // 等待写入 SourceBuffer 的 Uint8Array 队列
let isUpdating = false;        // SourceBuffer 当前是否正在 appendBuffer

/**
 * 每开始一轮新回复时，重新创建流式音频播放器。
 */
const initAudioStream = () => {
    // 先停止上一轮可能还在播放的声音，并清空旧队列。
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    // MediaSource 允许 JavaScript 动态向媒体流中追加二进制数据。
    mediaSource = new MediaSource();
    audioPlayer.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
        try {
            // 后端 TTS 返回 mp3，因此浏览器端声明 audio/mpeg。
            sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');

            // appendBuffer 是异步的。
            // 当前块写完后触发 updateend，再继续消费下一块，避免并发写入报错。
            sourceBuffer.addEventListener('updateend', () => {
                isUpdating = false;
                processQueue();
            });
        } catch (e) {
            console.error("MSE AddSourceBuffer Error:", e);
        }
    });

    // 现代浏览器可能要求用户先产生点击等交互才允许自动播放声音。
    audioPlayer.play().catch(e => console.error("等待用户交互以播放音频"));
};

/**
 * 从 audioQueue 中取出一个音频块写入 SourceBuffer。
 *
 * 为什么一次只能 append 一个？
 * SourceBuffer 在 updating=true 时再次 appendBuffer 会抛异常，所以必须串行处理。
 */
const processQueue = () => {
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
        return;
    }

    isUpdating = true;
    const chunk = audioQueue.shift();
    try {
        sourceBuffer.appendBuffer(chunk);
    } catch (e) {
        console.error("SourceBuffer Append Error:", e);
        isUpdating = false;
    }
};

/**
 * 停止当前语音播放并释放浏览器资源。
 */
const stopAudio = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                mediaSource.endOfStream();
            } catch (e) {
                // 用户快速关闭时，MediaSource 状态可能已经变化，忽略即可。
            }
        }
        mediaSource = null;
    }

    // createObjectURL 创建的 URL 需要主动回收，避免长期使用页面时积累内存。
    if (audioPlayer.src) {
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

/**
 * 后端通过 JSON/SSE 只能方便地传字符串，所以二进制 MP3 会先编码为 Base64。
 * 这里把 Base64 恢复为 Uint8Array，再加入播放队列。
 */
const handleAudioChunk = (base64Data) => {
    try {
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);

        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        audioQueue.push(bytes);
        processQueue();
    } catch (e) {
        console.error("Base64 Decode Error:", e);
    }
};

// Vue 组件销毁时停止播放，避免用户已经离开页面声音还在继续。
onUnmounted(() => {
    stopAudio();
});

/**
 * 暴露给父组件：聊天窗口打开后可以自动聚焦输入框。
 */
function focus() {
  inputRef.value.focus()
}

/**
 * 发送一条消息。
 *
 * audio_msq 有值：说明文字来自语音识别组件；
 * audio_msq 无值：说明文字来自普通输入框。
 */
async function handleSend(event, audio_msq) {
  let content

  if (audio_msq) {
    content = audio_msq.trim()
  } else {
    content = message.value.trim()
  }

  // 空字符串不发请求，既节省模型费用，也避免产生无意义聊天记录。
  if (!content) return

  // 每轮对话开始前创建一条新的音频播放流。
  initAudioStream()

  // 本轮请求拥有自己的 id。
  // 后面如果 processId 被 close()/handleStop() 改掉，本轮迟到的数据会被丢弃。
  const curId = ++processId

  // 立即清空输入框，让交互感觉更灵敏。
  message.value = ''

  // “乐观更新 UI”：不用等后端返回，先把用户消息显示出来，
  // 再创建一个空的 AI 消息气泡，后续流式文本不断追加进去。
  emit('pushBackMessage', {
    role: 'user',
    content: content,
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

      // 一次回调通常只收到一个很小的数据块。
      onmessage(data, isDone) {
        // 用户已经停止/关闭了这一轮，就忽略旧流后续到达的数据。
        if (curId !== processId) return

        // 文本块：追加到最后一个 AI 气泡，实现“打字机式”回复。
        if (data.content) {
          emit('addToLastMessage', data.content)
        }

        // 音频块：Base64 -> Uint8Array -> MediaSource 队列。
        if (data.audio) {
          handleAudioChunk(data.audio)
        }

        // isDone=true 表示收到了 [DONE]。
        // 当前实现不需要额外 UI 操作，所以这里只保留参数供后续扩展使用。
        if (isDone) {
          // 例如未来可以在这里关闭“AI 正在输入”的 loading 状态。
        }
      },

      onerror(err) {
        console.error('聊天流请求失败:', err)
      },
    })
  } catch (err) {
    console.error('发送消息失败:', err)
  }
}

/**
 * 聊天弹窗关闭时：
 * 1. 让当前流的数据失效；
 * 2. 退出麦克风模式；
 * 3. 停止 TTS。
 */
function close() {
  ++processId
  showMic.value = false
  stopAudio()
}

/**
 * 用户点击“停止”时不一定关闭整个聊天框，只终止本轮数据与声音。
 */
function handleStop() {
  ++processId
  stopAudio()
}

// defineExpose 让父组件通过 ref 调用 inputField.focus() / inputField.close()。
defineExpose({
  focus,
  close,
})
</script>

<template>
  <!--
    @submit.prevent：拦截浏览器表单默认刷新行为，改为调用 handleSend。
    v-if / v-else：文字输入和麦克风输入两个界面互斥显示。
  -->
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

    <!-- 点击纸飞机和按 Enter 最终都会执行 handleSend。 -->
    <div @click="handleSend" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon />
    </div>

    <!-- 切换为语音输入界面。 -->
    <div @click="showMic = true" class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
  </form>

  <!--
    Microphone 识别完成后 emit('send', text)，这里会再次进入同一个 handleSend，
    所以“文字输入”和“语音输入”最终共用完全相同的聊天后端链路。
  -->
  <Microphone
      v-else
      @close="showMic = false"
      @send="handleSend"
      @stop="handleStop"
  />
</template>

<style scoped>

</style>
