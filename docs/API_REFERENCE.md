# AiFriends API Reference（第四轮教学版）

> 本文以当前 `backend/web/urls.py` 和真实 View 为准。
>
> 学习目标不是背 URL，而是能回答：**谁发请求、是否认证、数据放哪里、正常/异常状态码是什么、返回 JSON 还是 SSE。**

---

# 1. 本地 Base URL：第四轮为什么看起来“没有后端地址”？

Vite 开发模式现在使用代理：

```text
Browser http://localhost:5173
        ↓ /api/... /media/...
Vite proxy
        ↓
Django http://127.0.0.1:8000
```

所以前端开发代码可以直接写：

```js
api.get('/api/health/')
```

而不是每个组件都写死：

```text
http://127.0.0.1:8000
```

这降低了第一次学习 CORS / Cookie host 的干扰。

直接用 curl / Postman 请求 Django 时，仍然使用：

```text
http://127.0.0.1:8000
```

---

# 2. 当前 API 总表

| Method | Path | Auth | Request | Response | 作用 |
|---|---|---|---|---|---|
| GET | `/api/health/` | 否 | - | JSON | 健康状态 / AI mode |
| POST | `/api/user/account/register/` | 否 | JSON | JSON + Cookie | 注册 |
| POST | `/api/user/account/login/` | 否 | JSON | JSON + Cookie | 登录 |
| POST | `/api/user/account/refresh_token/` | Cookie | empty | JSON + Cookie | 换 access |
| POST | `/api/user/account/logout/` | Bearer | empty | JSON | 撤销 refresh token + 删除 Cookie |
| GET | `/api/user/account/get_user_info/` | Bearer | - | JSON | 当前用户 |
| POST | `/api/user/profile/update/` | Bearer | multipart | JSON | 更新资料 |
| POST | `/api/create/character/create/` | Bearer | multipart | JSON | 创建 Character |
| POST | `/api/create/character/update/` | Bearer | multipart | JSON | 更新自己的 Character |
| POST | `/api/create/character/remove/` | Bearer | JSON | JSON | 删除自己的 Character |
| GET | `/api/create/character/get_single/` | Bearer | query | JSON | 编辑页读取 Character |
| GET | `/api/create/character/get_list/` | 视当前实现 | query | JSON | 用户 Character 列表 |
| GET | `/api/create/character/voice/get_list/` | Bearer | - | JSON | Voice 列表 |
| GET | `/api/homepage/index/` | 否 | query | JSON | 首页 / 搜索 |
| POST | `/api/friend/get_or_create/` | Bearer | JSON | JSON | 创建/读取 Friend |
| POST | `/api/friend/remove/` | Bearer | JSON | JSON | 删除 Friend |
| GET | `/api/friend/get_list/` | Bearer | query | JSON | Friend 列表 |
| POST | `/api/friend/message/chat/` | Bearer | JSON | **SSE** | AI Chat |
| GET | `/api/friend/message/get_history/` | Bearer | query | JSON | 历史消息 |
| POST | `/api/friend/message/asr/asr/` | Bearer | multipart | JSON | PCM → Text |

---

# 3. HTTP 状态码：第四轮开始不要只看 `result`

项目早期很多业务错误仍返回 HTTP 200。工程进阶阶段开始逐步使用更准确的 HTTP status。

当前认证/核心新增接口已经出现：

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
404 Not Found
409 Conflict
413 Payload Too Large
502 Bad Gateway
503 Service Unavailable
```

## 为什么前端既要看 status，又可能要看 JSON？

HTTP status 回答：

> 这是哪一类网络/API 结果？

JSON 中的 `result/message/code` 回答：

> 具体发生了什么业务问题？

Chapter 15 会继续把其他旧 API 逐步重构成统一错误结构。

---

# 4. JWT 认证协议

## 4.1 Access Token

前端 Pinia 保存 access：

```text
frontend/src/stores/user.js
```

普通 API / SSE 都在 Header 带：

```http
Authorization: Bearer <access-token>
```

## 4.2 Refresh Token

Refresh 放 HttpOnly Cookie。

JavaScript 不直接读取内容；浏览器通过 Cookie 自动带到：

```text
POST /api/user/account/refresh_token/
```

第四轮后 Cookie 策略集中在：

```text
backend/web/views/user/account/cookies.py
```

开发 `DEBUG=true` 时：

```text
secure=false
```

生产 HTTPS + `DEBUG=false` 时：

```text
secure=true
```

## 4.3 普通 Axios 与 SSE 共用同一次 Refresh

核心文件：

```text
frontend/src/js/http/authRefresh.js
frontend/src/js/utils/singleFlight.js
```

并发：

```text
A → 401
B → 401
C → 401
      ↓
只启动 1 个 refresh Promise
      ↓
拿新 access → Pinia
      ↓
A/B/C 使用新 token 重试
```

旧版 SSE 曾存在“refresh 返回成功但没有把新 access 写回 Pinia”的问题，第四轮将 Axios/SSE 收敛到同一个 `refreshAccessToken()`。

---

# 5. Health API

```http
GET /api/health/
```

无需登录。

Mock 模式示例：

```json
{
  "status": "ok",
  "database": "ok",
  "ai_mode": "mock",
  "features": {
    "rag": false,
    "asr": false,
    "tts": false
  },
  "request_id": "..."
}
```

Response Header 同时包含：

```http
X-Request-ID: ...
```

这个接口故意不返回：

```text
API_KEY
数据库密码
完整异常堆栈
私人数据
```

数据库不可用时预期：

```text
HTTP 503
status = degraded
```

---

# 6. 注册

```http
POST /api/user/account/register/
Content-Type: application/json
```

Body：

```json
{
  "username": "alice",
  "password": "secret123"
}
```

## 成功

```text
HTTP 201 Created
```

```json
{
  "result": "success",
  "access": "<jwt>",
  "user_id": 1,
  "username": "alice",
  "photo": "/media/...",
  "profile": "..."
}
```

同时设置 refresh HttpOnly Cookie。

## 错误

空输入：

```text
HTTP 400
```

重复用户名：

```text
HTTP 409 Conflict
```

## 为什么必须 `create_user()`？

```python
User.objects.create_user(...)
```

会 hash password。

不要：

```python
User.objects.create(password='123456')
```

Chapter 14 自动测试会验证数据库里不是明文密码。

---

# 7. 登录

```http
POST /api/user/account/login/
Content-Type: application/json
```

Body：

```json
{
  "username": "alice",
  "password": "secret123"
}
```

核心：

```python
user = authenticate(username=username, password=password)
```

成功：

```text
HTTP 200
access JSON + refresh Cookie
```

用户名/密码为空：

```text
HTTP 400
```

用户名或密码错误：

```text
HTTP 401
```

---

# 8. Refresh

```http
POST /api/user/account/refresh_token/
Cookie: refresh_token=...
```

Body 可以为空：

```json
{}
```

成功：

```json
{
  "result": "success",
  "access": "<new access>"
}
```

并轮换 refresh cookie。当前启用了 SimpleJWT token blacklist：**本次已经使用过的旧 refresh token 会立即进入 blacklist，不能再次重放换取 access。**

缺少 / 过期 / 已撤销：

```text
HTTP 401
```

---

# 9. Logout

```http
POST /api/user/account/logout/
Authorization: Bearer <access>
```

成功：

```json
{
  "result": "success"
}
```

后端会先将当前 refresh token 加入 blacklist，再删除 refresh cookie；前端同时清 Pinia。仅删除 Cookie 不等于撤销凭证，所以服务端 blacklist 是 logout 安全语义的一部分。

---

# 10. Get Current User

```http
GET /api/user/account/get_user_info/
Authorization: Bearer <access>
```

成功：

```json
{
  "result": "success",
  "user_id": 1,
  "username": "alice",
  "photo": "/media/...",
  "profile": "..."
}
```

浏览器刷新后，Pinia 内存丢失时，`api.js` 可以先通过 refresh 恢复 access，再完成该请求。

---

# 11. Profile Update

```http
POST /api/user/profile/update/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

FormData：

```text
username
profile
photo?       optional
```

上传头像会在写入前校验真实图片内容，只接受 JPEG / PNG / WebP，单张最多 8 MB、最多 2500 万像素；数据库中的用户名与 UserProfile 元数据使用事务保持一致。

这个 API 仍然是 Chapter 15 很好的 Serializer 重构对象。

---

# 12. Character Create

```http
POST /api/create/character/create/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

字段：

```text
name
voice_id
profile
photo
background_image
```

数据流：

```text
Vue FormData
 ↓
request.data + request.FILES
 ↓
UserProfile
 ↓
Voice
 ↓
图片格式 / 大小 / 像素校验
 ↓
Character.objects.create
 ↓
SQLite + media
```

---

# 13. Character Update

```http
POST /api/create/character/update/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

字段：

```text
character_id
name
voice_id
profile
photo?             optional
background_image?  optional
```

后端必须重新检查：

```text
Character.author.user == request.user
```

这就是 Object-level Authorization。

---

# 14. Homepage

```http
GET /api/homepage/index/?items_count=0&search_query=...
```

无需登录。

分页当前是 offset 风格：

```text
items_count : items_count + 20
```

搜索：

```text
name icontains
OR
profile icontains
```

---

# 15. Friend Get or Create

```http
POST /api/friend/get_or_create/
Authorization: Bearer <access>
Content-Type: application/json
```

Body：

```json
{
  "character_id": 12
}
```

Friend 的业务含义：

```text
当前用户 × 某个 Character
```

同时也是：

```text
长期记忆边界
聊天历史边界
```

Chapter 18 会继续学习数据库 `UniqueConstraint`，避免并发时产生重复 Friend。

---

# 16. Friend List / Remove

列表：

```http
GET /api/friend/get_list/?items_count=0
Authorization: Bearer <access>
```

删除：

```http
POST /api/friend/remove/
Authorization: Bearer <access>
```

所有 Friend 私有操作都必须通过：

```text
friend.me.user == request.user
```

限制。

---

# 17. Chat：这是最重要的 API

```http
POST /api/friend/message/chat/
Authorization: Bearer <access>
Content-Type: application/json
```

Body：

```json
{
  "friend_id": 3,
  "message": "你好"
}
```

空消息：

```text
HTTP 400
```

Friend 不存在/不属于用户：

```text
HTTP 404
```

## Response 不是完整 JSON

```http
Content-Type: text/event-stream
```

事件：

```text
data: {"content":"你"}

data: {"content":"好"}

data: {"audio":"...base64..."}

data: {"error":"..."}

data: [DONE]

```

---

# 18. Chat 的 AI_MODE 行为

## Mock

```env
AI_MODE=mock
```

Chat 不创建真实 `CharGraph`，本地生成确定性回复。

但仍然经过：

```text
JWT
Friend ownership
SystemPrompt / history assembly
StreamingHttpResponse
SSE
Vue onmessage
Message DB
```

所以它非常适合 Chapter 00–07 与 CI。

## Text

```env
AI_MODE=text
```

真实 LLM + SSE，但默认：

```text
RAG off
ASR off
TTS off
```

## Full

默认完整：

```text
LLM
RAG Tool
ASR
TTS
```

可继续用 Feature Flag 单独覆盖。

---

# 19. Chat 的 SSE Refresh

请求建立时 access 过期：

```text
SSE HTTP 401
 ↓
refreshAccessToken()
 ↓
Pinia 写入新 access
 ↓
旧 SSE reject
 ↓
重新 startFetch()
 ↓
重新构建 Authorization Header
```

这点与“让 fetch-event-source 自己用旧 headers 自动重试”不同。

---

# 20. Chat Cancellation

前端：

```text
AbortController
```

传给：

```text
streamApi(... signal)
```

用户 Stop：

```text
controller.abort()
 ↓
SSE 连接关闭
 ↓
Django generator finally
 ↓
cancel_event.set()
 ↓
worker 尽快停止 LLM/TTS chunk
```

注意：第三方模型服务是否能做到“立刻终止远端计算”，还取决于 provider/API 行为。这是 Chapter 17 的工程讨论点。

---

# 21. Chat Message Persistence

正常完成后保存：

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
```

目前用户取消时不会走正常完成保存路径。

正常完成路径会先 `Message.objects.create(...)`，然后才发送 SSE `[DONE]`，避免客户端收到完成标记立即断开时丢失最后一条消息。

Chapter 17 Challenge：设计：

```text
partial=true
cancel_reason
```

等字段。

---

# 22. History

```http
GET /api/friend/message/get_history/?friend_id=3&last_message_id=0
Authorization: Bearer <access>
```

首次：

```text
last_message_id=0
```

继续向上翻：

```text
pk < last_message_id
```

每次最多 10 条 Message 记录。`last_message_id` 非整数/负数返回 HTTP 400；Friend 不存在或不属于当前用户返回 HTTP 404。

后端额外限制：

```text
friend__me__user=request.user
```

避免读取其他用户历史。

---

# 23. ASR

```http
POST /api/friend/message/asr/asr/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

字段：

```text
audio = PCM file
```

如果：

```env
ENABLE_ASR=false
```

返回：

```text
HTTP 503
```

```json
{
  "result": "ASR 未启用。请在 .env 中设置 ENABLE_ASR=true。"
}
```

这样文本学习不会因为没有 Speech Account 莫名失败。启用 ASR 后，PCM 上传在读取前限制为最多 **5 MB**；超过限制返回 HTTP 413，第三方 ASR Provider 调用失败返回 HTTP 502。

---

# 24. TTS 为什么没有单独 HTTP Endpoint？

TTS 是 Chat 内部并行任务：

```text
LLM chunk
 ├─ Queue → SSE content
 └─ TTS WebSocket
       ↓
     MP3 bytes
       ↓ Base64
     Queue → SSE audio
```

如果：

```env
ENABLE_TTS=false
```

Chat 直接走 `text_sender()`，不会连接 WSS。

如果 Character 没有 Voice，也自动退化到 text-only。

---

# 25. RAG 不是一个直接给浏览器调用的 API

它目前被封装为 LangGraph Tool：

```text
search_knowledge_base(query)
```

只有：

```env
ENABLE_RAG=true
```

才注册进 Agent Tool List。

这使 text 模式不需要先创建 LanceDB。

---

# 26. Request ID

第四轮加入 middleware：

```text
backend/web/middleware.py
```

客户端可以主动发送：

```http
X-Request-ID: my-debug-id
```

否则服务端自动生成。

Response：

```http
X-Request-ID: <same-id>
```

以后日志中可以用它把：

```text
HTTP
LLM
RAG
TTS
error
```

串成同一请求。

---

# 27. 用 curl 学 API

## Health

```bash
curl http://127.0.0.1:8000/api/health/
```

## Register

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' \
  http://127.0.0.1:8000/api/user/account/register/
```

Windows PowerShell 建议使用 `Invoke-RestMethod` 或在 DevTools 中学习，不必纠结 shell 引号差异。

---

# 28. 用 DevTools 学 API

F12 → Network。

每条请求至少看：

```text
Request URL
Method
Status
Request Headers
Request Payload / Form Data
Response Headers
Response / EventStream
```

认证问题再打开：

```text
Application → Cookies
```

---

# 29. 常见分层诊断

## 没有 Network 请求

前端事件/状态问题。

## 400

输入 validation / request body。

## 401

access / refresh / Authorization。

## 404

URL 或对象/ownership。

## 409

业务冲突，例如用户名重复。

## 500

先看 Django traceback。

## 503

某项依赖能力未准备，例如 ASR disabled / health DB degraded。

## SSE 200 但无 chunk

继续查：

```text
AI_MODE
worker
LLM
Queue
TTS
```

---

# 30. API 与源码索引

```text
backend/web/urls.py
```

认证：

```text
backend/web/views/user/account/
frontend/src/js/http/api.js
frontend/src/js/http/authRefresh.js
frontend/src/js/http/streamApi.js
```

Chat：

```text
backend/web/views/friend/message/chat/chat.py
backend/web/views/friend/message/chat/graph.py
```

AI Config：

```text
backend/web/ai/config.py
```

Memory：

```text
backend/web/views/friend/message/memory/
```

RAG：

```text
backend/web/documents/utils/
```

Health / Request ID：

```text
backend/web/views/health.py
backend/web/middleware.py
```

前端聊天：

```text
InputField.vue
Microphone.vue
```

---

# 31. 下一阶段：OpenAPI / Swagger

当前本文是手工维护的教学版 API Reference。

Chapter 15 后可以继续加入：

```text
Serializer
OpenAPI schema
Swagger UI
错误码表
请求/响应 example
```

然后比较：

```text
自动生成 API 文档
vs
面向学习者的解释文档
```

两者不是互相替代：机器 schema 负责精确，教学文档负责解释“为什么”。
