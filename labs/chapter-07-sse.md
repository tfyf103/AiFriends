# Chapter 07 Lab：SSE 流式聊天与 Message 落库

## 本章目标

把上一章的：

```text
等完整答案 → 一次性 JSON
```

升级为：

```text
模型产生一小段 → Django 立刻 yield → 浏览器立刻显示
```

并在结束后把完整问答和 token 用量保存到 `Message`。

---

## 历史检查点

```text
b9ea1c3404b04413d638067de78c3ed4d7262fc3  后端流式输出
3c7c464b51dcbb411ad50bafe58ad214ecc6eb2c  前端流式回复
ea419695f4d8e9e2cec97c4f92a03dc7d679e4df  聊天记录流式加载
```

重点比较：

```bash
git diff 72a9866e3370481a8fa6e070e55c7784977c058a b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

---

## TODO 1：先手写一个假的 SSE

先不调用 LLM。

写一个 generator：

```python
def event_stream():
    yield 'data: {"content":"你"}\n\n'
    yield 'data: {"content":"好"}\n\n'
    yield 'data: [DONE]\n\n'
```

用：

```python
StreamingHttpResponse(
    event_stream(),
    content_type='text/event-stream',
)
```

### 验收

浏览器能逐事件收到：

```text
你
好
[DONE]
```

先证明 SSE 协议工作，再把 LLM 放进去。

---

## TODO 2：理解 SSE framing

每条事件：

```text
data: ...\n\n
```

为什么是两个换行？

因为空行表示一个 SSE event frame 结束。

### 主动错误实验

把 `\n\n` 改成 `\n`，观察浏览器是否迟迟不触发 message。

恢复正确格式。

---

## TODO 3：把 `invoke` 改成 `stream`

尝试：

```python
for msg, metadata in app.stream(
    inputs,
    stream_mode='messages',
):
    ...
```

只处理：

```python
BaseMessageChunk
```

有内容时：

```python
yield f'data: {json.dumps({"content": msg.content})}\n\n'
```

### 验收

Network 中一个 HTTP 请求持续打开，但 UI 在请求结束前已经不断出现内容。

---

## TODO 4：前端 `fetchEventSource`

不要用普通 `axios.post()` 等完整 response。

理解：

```js
onopen()
onmessage()
onerror()
onclose()
```

遇到：

```text
[DONE]
```

不要 `JSON.parse('[DONE]')`。

### 验收

每收到一个：

```json
{"content": "片段"}
```

就追加到最后一个 AI Message。

---

## TODO 5：乐观 UI

用户点击发送后立即：

```text
history.push(userMessage)
history.push(emptyAiMessage)
```

后续 token 不断加到最后一条 AI Message：

```text
''
'你'
'你好'
'你好，'
'你好，我...'
```

### 思考

为什么不是每个 token 创建一条新聊天气泡？

---

## TODO 6：保存完整 Message

流式过程中维护：

```python
final_output = ''
final_usage = {}
```

每个 chunk：

```python
final_output += msg.content
```

结束后：

```python
Message.objects.create(...)
```

至少保存：

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
```

### 验收

数据库中 output 是完整一句，而不是最后一个 token。

---

## TODO 7：聊天历史分页

实现：

```text
GET /api/friend/message/get_history/
```

请求参数：

```text
friend_id
last_message_id
```

逻辑：

```text
last_message_id = 0 → 最新一批
last_message_id > 0 → 查询 id < last_message_id 的更老记录
```

前端向上滚动时加载旧消息。

### 难点验收

加载更老内容后，用户视口不能突然跳到列表顶部。

提示：记录插入前后的：

```text
scrollHeight
scrollTop
```

---

## TODO 8：SSE 的 JWT 过期

普通 Axios 有拦截器，但 SSE 使用另一套客户端。

实验：让 access 失效后发起聊天。

流程应该是：

```text
SSE onopen → 401
       ↓
refresh access
       ↓
重新建立 SSE 请求
```

理解为什么“已经关闭/失败的流”不能像普通 JSON response 那样凭空继续。

---

## 参考答案思路

后端：

```text
LLM stream
  ↓
for chunk
  ↓
yield SSE
  ↓
StreamingHttpResponse
```

前端：

```text
fetchEventSource
  ↓ onmessage
parse event
  ↓
更新 reactive history
  ↓
Vue 重新渲染最后一条气泡
```

---

## 常见错误

### 后端在 yield，但前端最后一次性出现

检查：

- `text/event-stream`
- 反向代理 buffering
- `X-Accel-Buffering: no`
- SSE event 是否正确以空行结束

### `[DONE]` JSON parse error

先判断特殊结束标记，再解析 JSON。

### 切换好友后旧回复继续写到新聊天

需要取消旧流或用 process id / AbortController 忽略陈旧回调。

### 保存的 AI output 为空

你只 yield 了 chunk，却没有同步累积 `final_output`。

---

## Challenge

为流式聊天增加四个前端状态：

```text
idle
connecting
streaming
error
```

并在 UI 上分别显示不同状态。

这会让你开始从“能跑”转向真正的产品级交互设计。
