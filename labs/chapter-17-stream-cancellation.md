# Chapter 17 Lab：异步、流、取消与资源释放

## 本章目标

理解“用户点击停止”不只是 UI 状态，而是一条跨层取消链路。

第四轮真实实现：

```text
InputField.vue AbortController
        ↓
streamApi signal
        ↓
浏览器关闭 SSE
        ↓
Django StreamingHttpResponse generator close
        ↓
cancel_event.set()
        ↓
LLM/TTS worker 尽快停止
```

---

## TODO 1：对比旧 Stop 与新 Stop

旧逻辑：

```text
processId++
忽略迟到数据
停止本地 Audio
```

它只解决“别显示了”。

新逻辑增加：

```js
AbortController.abort()
```

回答：

> 为什么“UI 不显示”不代表“不再消耗模型 token”？

---

## TODO 2：观察 Network

发送一个较长问题，在模型生成时点击停止。

DevTools → Network：

- SSE 请求是否结束？
- 结束时间是否接近点击时间？
- Console 是否出现 AbortError？

当前 `streamApi.js` 应把正常 Abort 当作正常控制流，而不是红色业务错误。

---

## TODO 3：理解 Queue

后端存在两个世界：

```text
Django 同步 generator
asyncio LLM / WebSocket
```

Queue 是桥：

```text
async worker → Queue → sync SSE generator
```

画出：

```text
谁 put？
谁 get？
None sentinel 是什么？
cancel_event 与 sentinel 有什么不同？
```

---

## TODO 4：处理异常

模拟：

```text
LLM 连接失败
TTS 连接失败
浏览器中途关闭
```

要求不会出现：

- generator 永久卡在 `mq.get()`；
- worker 没有结束信号；
- 前端无限重试；
- 页面把正常 Abort 当致命错误。

---

## TODO 5：思考“保存半截回复”

当前正常完成才保存完整 Message。

设计三种策略并比较：

```text
A. 用户取消就不保存
B. 保存 partial=true 的半截回复
C. 保存用户消息，但 AI output 标记 cancelled
```

数据库需要增加什么字段？历史 UI 怎么显示？Memory 是否应该吃进半截回复？

---

## TODO 6：超时

加入：

```text
LLM timeout
TTS handshake timeout
overall chat timeout
```

解释 timeout 与 user cancel 的区别。

---

## 验收

- [ ] Stop 后 Network 流真正结束；
- [ ] 能解释 AbortController；
- [ ] 能解释 Queue + sentinel；
- [ ] 后端不会因为取消永久阻塞；
- [ ] 能设计 partial message 策略；
- [ ] 能区分 cancel / timeout / failure。

---

## Challenge

把 cancellation reason 传入后端日志：

```text
user_stop
route_change
new_message
browser_disconnect
timeout
```

并统计哪一种最常见。
