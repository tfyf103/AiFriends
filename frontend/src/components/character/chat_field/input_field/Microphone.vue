<script setup>
import KeyboardIcon from '@/components/character/icons/KeyboardIcon.vue'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { MicVAD } from '@ricky0123/vad-web'
import api from '@/js/http/api.js'
import CONFIG_API from '@/js/config/config.js'

const emit = defineEmits(['close', 'send', 'stop'])
const isSpeaking = ref(false)
let vadInstance = null

const startRecording = async () => {
  const baseUrl = CONFIG_API.VAD_URL
  try {
    vadInstance = await MicVAD.new({
      // The package loads its worklet/model separately from the ONNX Runtime WASM
      // files. `npm run setup:vad` prepares both directories for local development.
      baseAssetPath: baseUrl,
      onnxWASMBasePath: `${baseUrl}onnx/`,
      onSpeechStart: () => {
        isSpeaking.value = true
        emit('stop')
      },
      onSpeechEnd: (audio) => {
        isSpeaking.value = false
        sendToBackend(float32ToInt16(audio))
      },
      positiveSpeechThreshold: 0.8,
      negativeSpeechThreshold: 0.65,
      minSpeechFrames: 5,
      redemptionFrames: 5,
    })

    await vadInstance.start()
  } catch (error) {
    console.error('VAD 初始化失败。先运行 npm run setup:vad：', error)
  }
}

const float32ToInt16 = (float32Array) => {
  const buffer = new Int16Array(float32Array.length)
  for (let i = 0; i < float32Array.length; i++) {
    const sample = Math.max(-1, Math.min(1, float32Array[i]))
    buffer[i] = sample < 0 ? sample * 0x8000 : sample * 0x7fff
  }
  return buffer.buffer
}

const sendToBackend = async (arrayBuffer) => {
  const formData = new FormData()
  formData.append('audio', new Blob([arrayBuffer], { type: 'audio/pcm' }), 'voice.pcm')

  try {
    const res = await api.post('/api/friend/message/asr/asr/', formData)
    if (res.data.result === 'success') {
      emit('send', null, res.data.text)
    }
  } catch (error) {
    console.error('ASR 请求失败:', error)
  }
}

onMounted(startRecording)

onBeforeUnmount(() => {
  vadInstance?.destroy()
  vadInstance = null
})
</script>

<template>
  <div class="absolute bottom-4 left-2 h-12 w-86 flex items-center bg-black/30 backdrop-blur-sm rounded-2xl">
    <div v-if="isSpeaking" class="flex items-center justify-center gap-1 h-6 flex-1">
      <div
        v-for="i in 32"
        :key="i"
        class="w-0.5 bg-blue-400 rounded-full animate-wave"
        :style="{ animationDelay: `${i * 0.1}s` }"
      ></div>
    </div>
    <div v-else class="text-white/50 text-base w-full text-center">语音输入</div>
    <button
      type="button"
      aria-label="切换回键盘输入"
      @click="emit('close')"
      class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer"
    >
      <KeyboardIcon />
    </button>
  </div>
</template>

<style scoped>
.animate-wave {
  height: 4px;
  animation: wave-animation 0.6s ease-in-out infinite alternate;
}

@keyframes wave-animation {
  0% { height: 4px; opacity: 0.3; }
  100% { height: 20px; opacity: 1; }
}
</style>
