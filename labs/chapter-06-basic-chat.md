# Chapter 06 Lab：最小 LLM Chat —— 先不要流式

## 本章目标

第一次把浏览器输入送进大模型。

这一章故意**不做 SSE、不做工具、不做记忆、不做语音**。

先建立最小闭环：

```text
Vue Input
  ↓ POST JSON
Django MessageChatView
  ↓
LangChain HumanMessage
  ↓
ChatOpenAI
  ↓
一次性结果
  ↓ JSON
Vue 显示回答
```

---

## 历史检查点

```text
72a9866e3370481a8fa6e070e55c7784977c058a  实现聊天后端
```

观察这个版本非常重要，因为后面所有复杂能力都是从这里长出来的。

---

## TODO 1：最小模型调用

在 Django shell 或临时脚本里先测试模型连接：

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
```

构造 LLM 后执行：

```python
res = llm.invoke([
    HumanMessage('你好，请只回答：连接成功')
])
```

### 验收

- [ ] API_KEY 可用
- [ ] API_BASE 可用
- [ ] model 名称可用
- [ ] 能打印 `res.content`

不要一开始就在 Vue/Django 全链路里调 API。先把外部依赖单独证明能用。

---

## TODO 2：实现 Chat API

接口：

```text
POST /api/friend/message/chat/
```

请求：

```json
{
  "friend_id": 1,
  "message": "你好"
}
```

检查：

1. message 不能是空字符串
2. Friend 必须属于当前登录用户
3. 把 message 转为 `HumanMessage`
4. 调模型
5. 返回 AI 文本

### 权限验收

手动改 `friend_id` 为其他用户的 Friend。

后端必须拒绝/找不到，而不是让你与别人的会话上下文交互。

---

## TODO 3：Vue 输入框

使用：

```js
const message = ref('')
```

表单：

```vue
<form @submit.prevent="handleSend">
```

发送后至少做：

```text
trim
空消息 return
发送请求
显示回答
```

### 验收

按 Enter 能发送；空格字符串不会请求后端。

---

## TODO 4：记录一次完整网络请求

打开 Network，记录：

```text
Request URL:
Method:
Authorization:
Request Payload:
Response:
Duration:
```

然后回答：

> 用户点击发送后，等待期间浏览器为什么没有任何 AI 内容可以显示？

答案：普通一次性 HTTP Response 要等模型调用完成后才获得完整响应体。

这正是下一章引入 SSE 的动机。

---

## TODO 5：故意增加延迟

仅在实验分支中临时：

```python
import time
time.sleep(3)
```

放在后端返回前。

观察 UI。

思考：

- 页面是假死了吗？
- HTTP 请求还在运行吗？
- 用户有没有办法知道模型已经生成前几个 token？

---

## 参考答案思路

最小 Chat 不需要 Agent：

```text
messages = [HumanMessage(message)]
res = llm.invoke(messages)
return Response({"content": res.content})
```

先把这条链路真正理解，再升级成：

```text
invoke → stream
JSON → SSE
LLM → LangGraph
单轮 → 多轮 + memory
```

---

## 常见错误

### 401

先看 JWT，不是模型问题。

### 500

先看 Django Traceback；常见是环境变量/模型连接异常。

### Model not found / 404 from API provider

模型名称与 API_BASE 对应服务不兼容。

### `res` 打印很复杂

LangChain 返回的是 Message 对象。你通常需要：

```python
res.content
```

---

## Challenge

给 API 增加：

```json
{
  "latency_ms": 1234
}
```

记录模型调用耗时。

然后思考：

> “总耗时变短”和“用户感觉更快”是不是同一件事？

下一章 SSE 不一定降低模型总生成时间，但能大幅改善首 token 等待体验。
