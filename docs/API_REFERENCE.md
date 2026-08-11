# AiFriends API Reference（新手版）

> 本文按当前 `backend/web/urls.py` 与对应 View 整理。
>
> 它不是为了替代源码，而是让你在做前后端联调时快速回答：**请求发到哪里、用什么 Method、要不要登录、参数放哪里、返回什么类型。**

---

# 1. 先理解 5 个基础概念

## 1.1 Base URL

本地 Vue 开发模式下，当前前端配置通常把后端指向：

```text
http://127.0.0.1:8000
```

所以：

```text
/api/user/account/login/
```

实际请求地址是：

```text
http://127.0.0.1:8000/api/user/account/login/
```

---

## 1.2 普通 JSON API

例如：

```http
POST /api/friend/get_or_create/
Content-Type: application/json
Authorization: Bearer <access-token>
```

Body：

```json
{
  "character_id": 1
}
```

前端通常通过：

```text
frontend/src/js/http/api.js
```

发送。

---

## 1.3 Multipart / 文件上传

涉及图片或音频时使用 `FormData`：

```js
const formData = new FormData()
formData.append('photo', file)
```

Django 中：

```python
request.data
request.FILES
```

是两个需要同时理解的入口。

典型接口：

- 更新用户头像
- 创建/更新 Character
- ASR 音频上传

---

## 1.4 JWT 认证

受保护接口需要：

```http
Authorization: Bearer <access-token>
```

项目使用：

```text
access token  → 前端 Store，放 Authorization Header
refresh token → HttpOnly Cookie，用于换新 access
```

普通请求由：

```text
frontend/src/js/http/api.js
```

统一处理。

SSE 聊天由：

```text
frontend/src/js/http/streamApi.js
```

单独处理流式请求和 Token 刷新重连。

---

## 1.5 SSE 不是普通 JSON Response

聊天接口：

```text
POST /api/friend/message/chat/
```

返回：

```http
Content-Type: text/event-stream
```

事件类似：

```text
data: {"content":"你"}

data: {"content":"好"}

data: {"audio":"...base64..."}

data: [DONE]

```

因此不能把它当普通 `axios.post(...).then(res => ...)` 的完整 JSON 响应来理解。

---

# 2. API 总表

| Method | Path | 登录 | 类型 | 作用 |
|---|---|---:|---|---|
| POST | `/api/user/account/login/` | 否 | JSON | 登录 |
| POST | `/api/user/account/logout/` | 是 | JSON | 退出并删除 refresh cookie |
| POST | `/api/user/account/register/` | 否 | JSON | 注册 |
| POST | `/api/user/account/refresh_token/` | Cookie | JSON | 用 refresh 换 access |
| GET | `/api/user/account/get_user_info/` | 是 | JSON | 获取当前用户资料 |
| POST | `/api/user/profile/update/` | 是 | multipart | 更新用户名/简介/头像 |
| POST | `/api/create/character/create/` | 是 | multipart | 创建角色 |
| POST | `/api/create/character/update/` | 是 | multipart | 更新自己的角色 |
| POST | `/api/create/character/remove/` | 是 | JSON | 删除自己的角色 |
| GET | `/api/create/character/get_single/` | 是 | query | 获取自己的单个角色供编辑 |
| GET | `/api/create/character/get_list/` | 视实现用途 | query | 获取角色列表 |
| GET | `/api/create/character/voice/get_list/` | 是 | query | 获取可用音色 |
| GET | `/api/homepage/index/` | 否 | query | 首页/搜索 Character |
| POST | `/api/friend/get_or_create/` | 是 | JSON | 建立或获取 Friend |
| POST | `/api/friend/remove/` | 是 | JSON | 删除自己的 Friend |
| GET | `/api/friend/get_list/` | 是 | query | 好友列表 |
| POST | `/api/friend/message/chat/` | 是 | JSON → SSE | AI 流式聊天 + TTS |
| GET | `/api/friend/message/get_history/` | 是 | query | 分页获取历史消息 |
| POST | `/api/friend/message/asr/asr/` | 是 | multipart | PCM 语音识别 |

---

# 3. 用户认证 API

## 3.1 注册

```text
POST /api/user/account/register/
```

### Body

```json
{
  "username": "alice",
  "password": "123456"
}
```

### 主要后端动作

```text
检查用户名/密码
  ↓
检查 username 是否存在
  ↓
User.objects.create_user(...)
  ↓
UserProfile.objects.create(...)
  ↓
生成 JWT refresh/access
```

### 成功响应核心字段

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

同时 response 设置：

```text
refresh_token HttpOnly Cookie
```

### 常见业务错误

```text
用户名或密码不能为空
用户名已存在
系统异常，请稍后重试
```

---

## 3.2 登录

```text
POST /api/user/account/login/
```

### Body

```json
{
  "username": "alice",
  "password": "123456"
}
```

### 核心逻辑

```python
user = authenticate(
    username=username,
    password=password,
)
```

成功后生成 JWT，并与注册接口类似返回用户资料。

### 新手调试

如果 UI 提示登录失败：

1. Network 看 Request Payload
2. 看 Response `result`
3. 登录成功后检查 `access`
4. 检查 Cookies 中 refresh_token
5. 再看后续请求有没有 Authorization Header

---

## 3.3 退出

```text
POST /api/user/account/logout/
```

需要登录。

后端主要动作：

```text
删除 refresh_token Cookie
```

前端同时需要清除 Pinia 中当前用户/access 状态。

---

## 3.4 刷新 Access Token

```text
POST /api/user/account/refresh_token/
```

前端无需在 JSON Body 中手工传 refresh token；当前设计从 Cookie 读取：

```python
request.COOKIES.get('refresh_token')
```

### 成功

```json
{
  "result": "success",
  "access": "<new-access-token>"
}
```

### 失败

典型 HTTP Status：

```text
401
```

典型原因：

```text
refresh token 不存在
refresh token 已过期/无效
```

---

## 3.5 获取当前用户

```text
GET /api/user/account/get_user_info/
```

### Header

```http
Authorization: Bearer <access-token>
```

### 成功

```json
{
  "result": "success",
  "user_id": 1,
  "username": "alice",
  "photo": "/media/...",
  "profile": "..."
}
```

这个接口很适合页面刷新后的用户状态恢复。

---

# 4. 用户资料 API

## 4.1 更新 Profile

```text
POST /api/user/profile/update/
```

需要登录。

使用 `multipart/form-data`。

### FormData

```text
username    必填
profile     必填
photo       可选，新头像
```

### 成功

```json
{
  "result": "success",
  "user_id": 1,
  "username": "new_name",
  "profile": "new profile",
  "photo": "/media/..."
}
```

### 权限

后端直接使用：

```python
request.user
```

因此不能通过上传一个 `user_id` 去修改别人资料。

---

# 5. Character API

## 5.1 创建 Character

```text
POST /api/create/character/create/
```

需要登录；`multipart/form-data`。

### FormData

```text
name              必填
voice_id          必填（当前版本）
profile           必填
photo             必填
background_image  必填
```

### 核心关系

```text
request.user
   ↓
UserProfile
   ↓ author
Character
   ↓ voice
Voice
```

### 成功

```json
{
  "result": "success"
}
```

---

## 5.2 更新 Character

```text
POST /api/create/character/update/
```

需要登录；`multipart/form-data`。

### FormData

```text
character_id      必填
name              必填
voice_id          必填
profile           必填
photo             可选
background_image  可选
```

### 权限核心

应理解为：

```python
Character.objects.get(
    id=character_id,
    author__user=request.user,
)
```

也就是即使浏览器伪造其它 id，也不能编辑别人的 Character。

---

## 5.3 删除 Character

```text
POST /api/create/character/remove/
```

### Body

```json
{
  "character_id": 1
}
```

权限同样必须约束当前登录用户。

---

## 5.4 获取单个 Character

```text
GET /api/create/character/get_single/?character_id=1
```

主要用于编辑页面加载当前角色。

返回核心结构类似：

```json
{
  "result": "success",
  "character": {
    "id": 1,
    "name": "Alice",
    "profile": "...",
    "photo": "/media/...",
    "background_image": "/media/...",
    "voice_id": 1
  },
  "voices": [
    {"id": 1, "name": "Voice A"}
  ]
}
```

---

## 5.5 获取 Voice 列表

```text
GET /api/create/character/voice/get_list/
```

成功：

```json
{
  "result": "success",
  "voices": [
    {
      "id": 1,
      "name": "音色名称"
    }
  ]
}
```

注意：前端一般只需要数据库 Voice 的 `id/name`；真正传给 TTS 的服务端 `voice_id` 保存在后端 Model 中。

---

# 6. Homepage / 搜索

## 6.1 首页列表

```text
GET /api/homepage/index/
```

### Query

```text
items_count=0
search_query=
```

示例：

```text
/api/homepage/index/?items_count=0&search_query=Alice
```

### 分页

后端每批当前按约 20 个 Character 读取。

下一页让：

```text
items_count = 当前前端已经有的条数
```

### 搜索

当前逻辑会在：

```text
Character.name
Character.profile
```

中做 `icontains` 模糊匹配。

### Character 响应结构核心

```json
{
  "id": 1,
  "name": "Alice",
  "profile": "...",
  "photo": "/media/...",
  "background_image": "/media/...",
  "author": {
    "user_id": 1,
    "username": "tfyf103",
    "photo": "/media/..."
  }
}
```

---

# 7. Friend API

## 7.1 Get or Create Friend

```text
POST /api/friend/get_or_create/
```

需要登录。

### Body

```json
{
  "character_id": 1
}
```

### 语义

```text
当前用户与 Character 已存在 Friend？
├── 是 → 返回已有关系
└── 否 → 创建 Friend 后返回
```

Friend 响应包含：

```text
friend.id
friend.character
```

其中 Character 又包含 author/photo/background/profile 等信息。

---

## 7.2 Friend List

```text
GET /api/friend/get_list/?items_count=0
```

需要登录。

当前查询核心：

```text
Friend.me == 当前用户
order_by(-update_time)
```

因此 Friend 的 `update_time` 可以用来表达“最近互动”。

---

## 7.3 Remove Friend

```text
POST /api/friend/remove/
```

### Body

```json
{
  "friend_id": 1
}
```

必须限制：

```text
friend.me == 当前用户
```

---

# 8. Chat API（项目核心）

## 8.1 AI Chat + SSE + TTS

```text
POST /api/friend/message/chat/
```

需要登录。

### Request JSON

```json
{
  "friend_id": 1,
  "message": "你好"
}
```

### 后端在返回流之前做什么？

```text
1. 验证 message 非空
2. 验证 Friend 属于 request.user
3. CharGraph.create_app()
4. HumanMessage(message)
5. 加 SystemPrompt
6. 加 Character.profile
7. 加 Friend.memory
8. 加最近历史 Message
```

### SSE 文本事件

```text
data: {"content":"你"}

```

### SSE 音频事件

```text
data: {"audio":"<base64 mp3 bytes>"}

```

### 结束

```text
data: [DONE]

```

### 结束以后后端还做什么？

保存：

```text
Message.friend
Message.user_message
Message.input
Message.output
Message.input_tokens
Message.output_tokens
Message.total_tokens
```

并在当前实现中按一定消息数量触发：

```text
update_memory(friend)
```

### Tool Calling

当前 `CharGraph` 工具包括：

```text
get_time
search_knowledge_base
```

如果 LLM 产生 tool_calls：

```text
agent → tools → agent
```

---

## 8.2 获取历史 Message

```text
GET /api/friend/message/get_history/
```

需要登录。

### Query

```text
friend_id=1
last_message_id=0
```

语义：

```text
last_message_id = 0
→ 获取最新一批

last_message_id > 0
→ 获取 id 更小的历史记录
```

响应中每条核心：

```json
{
  "id": 123,
  "user_message": "...",
  "output": "..."
}
```

前端再把一条数据库 Message 展开为两个 UI Message：

```text
user bubble
ai bubble
```

---

# 9. ASR API

## 9.1 Speech to Text

```text
POST /api/friend/message/asr/asr/
```

需要登录；`multipart/form-data`。

### FormData

```text
audio = PCM file/blob
```

### 当前后端期望的语音服务参数核心

```text
sample_rate: 16000
format: pcm
model: gummy-realtime-v1
```

### 成功

```json
{
  "result": "success",
  "text": "识别出来的文字"
}
```

前端把这个 text 重新交给普通聊天 `handleSend`，因此不会维护第二套 AI 对话业务。

---

# 10. 哪些能力不是 HTTP API？

## 10.1 Long-term Memory

不是浏览器直接调用的 endpoint。

触发于后端聊天结束后的内部逻辑：

```text
Message count 达到条件
   ↓
update_memory(friend)
   ↓
MemoryGraph
   ↓
Friend.memory
```

---

## 10.2 RAG 建库

`insert_documents()` 是离线/后台建库逻辑，不是当前面向浏览器的 REST endpoint：

```text
data.txt
 ↓ TextLoader
split
 ↓ Embedding
LanceDB
```

在线查询则由 `search_knowledge_base` Tool 在 LangGraph 内部触发。

---

## 10.3 TTS WebSocket

浏览器没有直接连接 TTS 服务。

当前结构：

```text
Browser
  ↕ SSE
Django
  ↕ WebSocket
TTS Service
```

这样第三方服务的 API Key 保留在后端。

---

# 11. 调试 API 的固定顺序

每次 API “不工作”，严格按这个顺序：

```text
1. 浏览器有没有发请求？
2. URL 对吗？
3. Method 对吗？
4. Body/Query/FormData 对吗？
5. Authorization 有吗？
6. HTTP Status 是什么？
7. Response 是什么？
8. Django 终端有没有 Traceback？
9. View 是否进入？
10. ORM 查询是否命中？
11. 外部 LLM/ASR/TTS/RAG 是否成功？
```

不要看到一句“系统异常”就从头乱改整个项目。

---

# 12. curl 思维练习

即使你主要用 Vue，也应该学会把前端与后端问题分开。

例如一个不需要登录的首页请求：

```bash
curl "http://127.0.0.1:8000/api/homepage/index/?items_count=0&search_query="
```

如果 curl 能成功，而 Vue 失败，问题更可能在：

```text
前端 URL
CORS
Axios 配置
状态处理
```

而不是 Django 核心业务。

对于需要 JWT 的接口，可用类似：

```bash
curl \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://127.0.0.1:8000/api/user/account/get_user_info/"
```

> 不要把真实 token 提交进 Git、Issue、截图或教程。

---

# 13. 源码索引

路由总表：

```text
backend/web/urls.py
```

认证：

```text
backend/web/views/user/account/
```

资料：

```text
backend/web/views/user/profile/
```

Character：

```text
backend/web/create/character/
```

Friend：

```text
backend/web/views/friend/
```

Chat：

```text
backend/web/views/friend/message/chat/
```

Memory：

```text
backend/web/views/friend/message/memory/
```

ASR：

```text
backend/web/views/friend/message/asr/
```

RAG：

```text
backend/web/documents/
```

做实验时建议：先看本文确定接口契约，再打开对应源码理解“为什么这样实现”。
