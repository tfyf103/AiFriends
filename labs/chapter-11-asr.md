# Chapter 11 Lab：ASR——从浏览器麦克风到文字

## 本章目标

让用户不打字，直接说话：

```text
Microphone
  ↓
浏览器音频
  ↓ 转 PCM 16k
FormData(audio)
  ↓ HTTP
Django ASRView
  ↓ WebSocket
ASR 服务
  ↓ transcription
Django JSON
  ↓
Vue 把文字当作普通聊天输入发送
```

---

## 历史检查点

```text
02cbc4f7567ebbed95eba483724611c35b6f6b1f  前端语音输入
5c0f6473fefad53542280257399d830663c8683a  后端语音识别
```

---

## TODO 1：先搞清 ASR 与 TTS

```text
ASR: Audio → Text
TTS: Text → Audio
```

本章只做 ASR。

如果你把两个方向混在一起，后面会很难调试。

---

## TODO 2：浏览器录音

拿到麦克风权限。

要求 UI 至少有：

```text
开始录音
停止录音
取消
```

### 验收

- [ ] 第一次浏览器会请求麦克风权限
- [ ] 拒绝权限时 UI 不崩溃
- [ ] 组件卸载时释放/停止录音资源

---

## TODO 3：理解采样率与 PCM

后端当前 ASR 参数：

```text
sample_rate = 16000
format = pcm
```

你的前端必须明确自己发的是什么。

思考：为什么不能随便把浏览器生成的任意 mp3/webm 文件标个 `.pcm` 后缀就认为它是 PCM？

文件扩展名不改变实际编码格式。

---

## TODO 4：上传音频

前端：

```js
const formData = new FormData()
formData.append('audio', blob, 'voice.pcm')
```

调用：

```text
POST /api/friend/message/asr/asr/
```

### 验收

Network 中 Content-Type 是 multipart/form-data；后端能：

```python
audio = request.FILES.get('audio')
```

---

## TODO 5：先把后端做成 echo 测试

在连接真实 ASR 前，先让后端返回：

```json
{
  "result": "success",
  "text": "ASR TEST"
}
```

前端收到后自动把 `ASR TEST` 当成一条消息发送。

### 为什么这样做？

先证明：

```text
录音组件 → HTTP → Vue Chat
```

链路正确，再接第三方 WebSocket。

---

## TODO 6：建立 WebSocket ASR Task

后端读取：

```python
api_key = os.getenv('API_KEY')
wss_url = os.getenv('WSS_URL')
```

建立：

```python
websockets.connect(...)
```

发送 `run-task` 配置：

```text
task_group: audio
task: asr
function: recognition
model: gummy-realtime-v1
sample_rate: 16000
format: pcm
```

### 验收

收到：

```text
task-started
```

以后才开始发送 PCM 数据。

---

## TODO 7：分块发送 PCM

项目当前：

```python
chunk = 3200
```

循环：

```python
await ws.send(pcm_data[i:i+chunk])
await asyncio.sleep(0.01)
```

### 思考

为什么实时语音协议通常不是把超大音频一次性全部塞进去？

- 流式处理
- 网络背压
- 实时返回
- 服务端协议要求

---

## TODO 8：并行发送与接收

不能：

```text
先把全部音频发完
再开始读返回值
```

使用：

```python
await asyncio.gather(
    asr_sender(...),
    asr_receiver(...),
)
```

理解 duplex：发送和接收可以同时发生。

---

## TODO 9：只拼接句子结束结果

事件：

```text
result-generated
```

检查：

```text
transcription.sentence_end
```

然后：

```python
text += transcription['text']
```

### 主动错误实验

把所有中间 partial transcription 都直接追加，看看最终文本是否重复。

---

## TODO 10：ASR 结果重新进入 Chat

前端拿到：

```json
{"text": "今天天气怎么样"}
```

不要建立第二套 AI Chat 流程。

直接调用已有：

```text
handleSend(..., audio_message)
```

也就是说：

```text
键盘输入 ─┐
          ├→ 同一个文字 Chat Pipeline
ASR文字 ──┘
```

这是复用业务逻辑的重要设计。

---

## 参考答案思路

把 ASR 当成**输入适配器**：

```text
不同输入方式
├── keyboard
└── microphone → ASR
              ↓
         normalized text
              ↓
        same chat system
```

AI 对话核心不应该关心文字原来是键盘敲的还是语音识别来的。

---

## 常见错误

### 浏览器麦克风没声音

先检查权限和设备，不要先改 Django。

### ASR 返回乱码/完全错误

重点检查实际音频编码、sample rate、channel、PCM 格式。

### WebSocket 401/鉴权失败

检查 API_KEY、Header 和服务地址。

### task-started 等不到

打印服务端文本事件，确认请求 payload 是否符合协议。

### 同一句识别重复多次

检查你是否把 partial result 与 sentence_end result 重复追加。

---

## Challenge

给录音 UI 增加音量/语音活动提示：

```text
静音
正在说话
句子结束
```

并思考 VAD（Voice Activity Detection）与 ASR 的区别：

- VAD：有没有人在说话
- ASR：说了什么
