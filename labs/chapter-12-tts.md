# Chapter 12 Lab：流式 TTS——文字生成的同时让角色开口

## 本章目标

把：

```text
LLM 完整文本生成完
  ↓
再一次性 TTS
```

升级为：

```text
LLM token chunk
  ├→ SSE 文本 → 浏览器显示
  └→ WebSocket TTS → MP3 chunk → SSE → 浏览器播放
```

用户会同时看到字、听到声音。

---

## 历史检查点

```text
845dcb620d0ce2f77f50b8c8dc94b91de338a58b  TTS 后端
8615f6607406be373ae9ce7b09934d5a4da496c6  前端播放声音
88343a97f0d74570e10bfe3952c0192669876a61  自定义角色音色
```

---

## TODO 1：先实现“完整文本 → 一次 TTS”

不要马上并发。

拿一句固定文本：

```text
你好，我是 AiFriends。
```

发送给 TTS 服务，保存/播放返回的 MP3。

### 验收

先证明：

- API_KEY 正确
- WSS_URL 正确
- voice_id 正确
- TTS 服务能返回音频

---

## TODO 2：理解为什么最终项目需要并行

如果流程是：

```text
LLM 5 秒
  ↓
TTS 3 秒
  ↓
8 秒后第一次听到声音
```

体验很差。

目标：LLM 生成前一小段后立刻喂给 TTS。

---

## TODO 3：建立 TTS WebSocket Task

发送：

```text
action: run-task
task_group: audio
task: tts
function: SpeechSynthesizer
model: cosyvoice-v3-flash
```

参数包括：

```text
voice
format: mp3
sample_rate: 22050
volume
rate
pitch
```

等待：

```text
task-started
```

---

## TODO 4：LLM Sender

使用：

```python
async for msg, metadata in app.astream(
    inputs,
    stream_mode='messages',
):
```

每有文本 chunk：

1. 发送给 TTS：`continue-task`
2. 同时放入本地 Queue：`{'content': ...}`

这样同一份 token 被两个消费者使用：

```text
LLM chunk
├→ TTS Service
└→ Browser text SSE
```

---

## TODO 5：TTS Receiver

WebSocket 如果收到：

```python
bytes
```

代表音频二进制。

当前项目将其转：

```python
audio = base64.b64encode(msg).decode('utf8')
```

再放入 Queue：

```python
{'audio': audio}
```

### 为什么 Base64？

因为当前 SSE payload 使用 JSON 文本事件；原始 bytes 不能直接塞进 JSON 字符串结构。

代价：Base64 会增加体积。

---

## TODO 6：为什么需要 Queue + Thread？

当前 Django SSE generator 是同步消费风格：

```python
while True:
    msg = mq.get()
    yield ...
```

而模型/TTS 使用 asyncio + WebSocket。

项目用：

```text
Thread
  ↓
asyncio.run(...)
  ↓
async tasks
  ↓
Queue
  ↓
同步 Django generator
```

实现桥接。

### 验收

你必须能解释 Queue 的两个世界：

```text
producer：async LLM/TTS
consumer：Django event_stream generator
```

---

## TODO 7：结束信号

Worker 无论成功失败都应：

```python
mq.put_nowait(None)
```

Consumer：

```python
msg = mq.get()
if not msg:
    break
```

最后：

```text
data: [DONE]
```

### 主动错误实验

去掉 `None` sentinel（只在实验分支）。

观察请求为什么可能一直不结束。

---

## TODO 8：前端 Base64 → bytes

```js
const binaryString = atob(base64Data)
const bytes = new Uint8Array(binaryString.length)
```

逐字节转换。

不要把 Base64 字符串本身直接当 MP3 bytes。

---

## TODO 9：MediaSource + SourceBuffer

创建：

```js
mediaSource = new MediaSource()
audioPlayer.src = URL.createObjectURL(mediaSource)
```

打开后：

```js
sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg')
```

MP3 chunk 到来：

```js
audioQueue.push(bytes)
processQueue()
```

### 为什么需要 queue？

`SourceBuffer` 正在 updating 时不能随意并发 appendBuffer。

所以：

```text
如果 updating → 等
updateend → 取下一块
```

---

## TODO 10：停止旧语音

切换好友/关闭聊天/点击停止时：

```text
pause audio
clear queue
endOfStream if possible
revokeObjectURL
ignore stale SSE callbacks
```

项目使用 `processId` 判断旧流回调是否已经失效。

### 验收

A 角色正在说话时关闭 A，再打开 B，A 的旧音频不能继续写进 B 的聊天体验。

---

## TODO 11：角色独立 Voice

不要在 TTS 中写死：

```text
voice='longanyang'
```

使用：

```python
friend.character.voice.voice_id
```

### 验收

两个角色配置不同 Voice 后，实际 TTS 音色不同。

---

## 参考答案思路

这章真正难点不是 TTS API，而是**并发数据流协调**：

```text
              ┌→ text SSE → UI
LLM stream ───┤
              └→ TTS WebSocket
                      ↓
                  audio bytes
                      ↓
                  Base64 SSE
                      ↓
                 MediaSource
```

你在构建的是一个小型流处理系统。

---

## 常见错误

### 文本正常、没有声音

分层检查：

1. TTS WebSocket 是否 task-started
2. 是否收到 bytes
3. SSE 是否包含 audio
4. 前端是否 decode
5. MediaSource 是否支持 `audio/mpeg`
6. 浏览器是否因为自动播放策略阻止 `play()`

### `SourceBuffer is updating`

没有串行处理 audio queue。

### 声音断断续续

检查 chunk 组织、网络延迟、播放 buffer 和是否错误 reset MediaSource。

### 关闭聊天后仍播放

资源清理不完整，或者旧异步回调仍有效。

---

## Challenge

测量三个时间：

```text
T0：点击发送
T1：第一个文本 token 出现
T2：第一段音频开始播放
```

分别计算：

```text
TTFT-text = T1 - T0
TTFA-audio = T2 - T0
```

然后尝试只优化“首音频延迟”，写出至少三个可能方向，而不是只关注总响应耗时。
