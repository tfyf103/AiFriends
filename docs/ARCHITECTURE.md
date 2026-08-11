# AiFriends 系统架构与请求链路

> 本文不再按“框架”讲，而是按 **数据到底怎么流动** 来解释整个系统。

---

# 1. 总体架构

```text
┌──────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                                                              │
│  Vue 3 + Router + Pinia + Axios + fetch-event-source        │
│                                                              │
│  页面 / 登录 / 角色 / 好友 / 聊天 / 麦克风 / 音频播放       │
└───────────────────────────┬──────────────────────────────────┘
                            │
                   HTTP JSON│SSE
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    Django + DRF Backend                      │
│                                                              │
│   URL ──► APIView ──► ORM / Service / AI                    │
│                                                              │
│   JWT Auth    Character CRUD    Friend    Message            │
└──────┬───────────────────┬───────────────────┬───────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌────────────┐     ┌────────────────┐    ┌──────────────────┐
│  SQLite    │     │ LangGraph      │    │ Speech WebSocket │
│            │     │                │    │                  │
│ User       │     │ Agent          │    │ ASR              │
│ Character  │     │ Tools          │    │ TTS              │
│ Friend     │     │ Memory Graph   │    │                  │
│ Message    │     └───────┬────────┘    └──────────────────┘
└────────────┘             │
                           ▼
                  ┌─────────────────┐
                  │ LLM / Embedding │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    LanceDB      │
                  │ Vector Storage  │
                  └─────────────────┘
```

---

# 2. 项目目录应该怎么读？

不要从第一个文件开始逐个看。

建议按职责读：

```text
AiFriends/
├── backend/
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py          # Django 总配置
│   │   └── urls.py              # Django 总 URL
│   └── web/
│       ├── urls.py              # 项目 API 路由表
│       ├── admin.py             # Django Admin 注册
│       ├── models/              # 数据库模型
│       ├── create/              # 角色创建/修改相关接口
│       ├── views/               # 页面/API业务逻辑
│       └── documents/           # RAG / LanceDB
│
└── frontend/
    ├── package.json
    ├── src/
    │   ├── main.js              # Vue 启动入口
    │   ├── router/              # 路由
    │   ├── stores/              # Pinia
    │   ├── js/
    │   │   ├── config/          # 前端环境地址
    │   │   └── http/            # Axios / SSE 封装
    │   ├── views/               # 页面级组件
    │   └── components/          # 可复用组件
    └── public/
```

---

# 3. 分层心智模型

## 前端

```text
View
  ↓
Component
  ↓
Store / Router
  ↓
HTTP Client
```

## 后端

```text
URL
  ↓
View
  ↓
Model / AI Service
  ↓
Database / External Service
```

## AI

```text
Messages
  ↓
LangGraph
  ↓
LLM
  ↓
Tool?
  ├─ no → answer
  └─ yes → ToolNode → LLM → answer
```

---

# 4. Vue 启动链路

```text
frontend/index.html
      ↓
frontend/src/main.js
      ↓
createApp(App)
      ↓
Pinia + Router
      ↓
App.vue
      ↓
RouterView
      ↓
具体页面
```

`main.js` 是前端真正入口。

---

# 5. 路由链路

`frontend/src/router/index.js` 把 URL 映射为页面：

```text
/                         HomepageIndex
/friend                   FriendIndex
/create                   CreateIndex
/user/profile             ProfileIndex
/user/account/login       LoginIndex
/user/account/register    RegisterIndex
```

并通过：

```text
meta.needLogin
```

标记页面是否需要登录。

---

# 6. 认证链路

```text
用户输入用户名密码
       ↓
Login API
       ↓
后端验证
       ↓
access token + refresh cookie/token
       ↓
Pinia 保存 accessToken
       ↓
api.js 请求拦截器
       ↓
Authorization: Bearer <token>
       ↓
DRF JWTAuthentication
       ↓
request.user
```

当 access token 过期：

```text
API 返回 401
   ↓
api.js response interceptor
   ↓
refresh_token API
   ↓
获得新 access token
   ↓
重新发送原请求
```

`isRefreshing + refreshSubscribers` 用于避免并发刷新风暴。

---

# 7. Django 请求路由

Django 总入口：

```text
backend/backend/urls.py
```

它 include：

```text
backend/web/urls.py
```

后者是实际业务 API 总表。

例如聊天：

```text
/api/friend/message/chat/
         ↓
MessageChatView
```

---

# 8. 数据模型关系

简化 ER：

```text
Django User
    │
    │ 1:1
    ▼
UserProfile
    │
    ├──────────────► Character
    │                    │
    │                    └────────► Voice
    │
    └──────────────► Friend ◄──── Character
                         │
                         ├────────► Message
                         │
                         └─ memory

SystemPrompt 独立存储系统提示词片段
```

---

# 9. 为什么 Friend 不是简单的 Character？

`Character` 是角色定义：

```text
名字
头像
背景
人格
声音
作者
```

`Friend` 是“某个用户与某个角色建立的关系”：

```text
me
character
memory
create_time
update_time
```

因此：

```text
Character = 角色模板
Friend    = 用户与角色之间的会话关系
```

长期记忆放在 Friend 上是合理的，因为不同用户与同一个角色可能拥有不同记忆。

---

# 10. 普通 JSON API 链路

例如一个普通接口：

```text
Vue Component
   ↓ api.post()
api.js
   ↓ Authorization
HTTP
   ↓
Django web/urls.py
   ↓
APIView
   ↓
ORM
   ↓
Response(JSON)
   ↓
Axios Promise
   ↓
Vue 更新状态
```

---

# 11. 聊天为什么是特殊链路？

因为它不是一次性 JSON。

```text
用户请求
   ↓
LLM 生成需要时间
   ↓
如果等完整答案
   ↓
用户几秒内什么都看不到
```

因此使用：

```text
StreamingHttpResponse + SSE
```

---

# 12. 聊天前端链路

入口：

```text
InputField.vue
```

用户点击发送：

```text
handleSend()
   ↓
先把 user message 推到 UI
   ↓
先创建空 ai message
   ↓
streamApi()
   ↓
POST /api/friend/message/chat/
```

这样用户不需要等服务器响应才能看到自己刚发送的消息。

---

# 13. `processId` 的作用

`InputField.vue` 使用递增 `processId`。

意义：

```text
请求 A 开始
   ↓
用户停止 / 发起新请求
   ↓
processId 改变
   ↓
请求 A 后续 chunk 到达
   ↓
发现 curId !== processId
   ↓
忽略旧数据
```

这是处理流式请求“过期结果”的一种简单方法。

---

# 14. `streamApi.js` 的职责

它不是普通 fetch。

职责包括：

```text
1. 加 Authorization
2. POST JSON
3. 检查 response 是否为 text/event-stream
4. 解析每条 SSE
5. 把 JSON 交给 onmessage
6. 处理 [DONE]
7. 处理 401 token 刷新
8. 控制异常重试
```

因此业务组件不需要重复写 SSE 解析代码。

---

# 15. 后端聊天入口完整链路

```text
MessageChatView.post()
     ↓
读取 friend_id + message
     ↓
验证 message 非空
     ↓
查询 Friend
     ↓
验证 Friend.me.user == request.user
     ↓
CharGraph.create_app()
     ↓
HumanMessage(message)
     ↓
add_system_prompt()
     ↓
add_recent_messages()
     ↓
event_stream()
     ↓
StreamingHttpResponse
```

---

# 16. Prompt 的实际组成

```text
SystemMessage
├── SystemPrompt(title='回复')
├── Character.profile
└── Friend.memory

HumanMessage / AIMessage
└── 最近数据库聊天历史

HumanMessage
└── 当前用户输入
```

最终类似：

```text
System: [系统规则 + 人格 + 长期记忆]
Human:  之前问题 1
AI:     之前回答 1
Human:  之前问题 2
AI:     之前回答 2
...
Human:  当前问题
```

---

# 17. LangGraph 图

```text
               ┌───────────────┐
               │     START     │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │     agent     │
               │   LLM invoke  │
               └───────┬───────┘
                       │
                 tool_calls?
                  /         \
                no           yes
                │             │
                ▼             ▼
             ┌─────┐    ┌────────────┐
             │ END │    │   tools    │
             └─────┘    │  ToolNode  │
                        └──────┬─────┘
                               │
                               └─────────► agent
```

---

# 18. Agent 节点

`model_call()`：

```text
state.messages
    ↓
llm.invoke()
    ↓
AIMessage
    ↓
加入 state.messages
```

模型如果想调用工具，AIMessage 中会出现 `tool_calls`。

---

# 19. Tool 节点

`ToolNode(tools)` 会读取模型的 tool call 并执行对应 Python 工具。

当前：

```text
get_time
search_knowledge_base
```

执行结果会作为 ToolMessage 进入 messages。

然后再次回到 agent。

---

# 20. RAG Tool 链路

```text
LLM 判断需要知识库
      ↓
search_knowledge_base(query)
      ↓
CustomEmbeddings.embed_query(query)
      ↓
Embedding API
      ↓
query vector
      ↓
LanceDB similarity_search(k=3)
      ↓
3 个 Document
      ↓
拼成 context string
      ↓
ToolMessage
      ↓
Agent 再次调用 LLM
      ↓
最终自然语言答案
```

---

# 21. 知识库构建链路

```text
data.txt
   ↓ TextLoader
Document
   ↓ RecursiveCharacterTextSplitter
chunks
   ↓ CustomEmbeddings.embed_documents
vectors
   ↓
LanceDB.from_documents
   ↓
lancedb_storage
```

切块参数当前：

```text
chunk_size = 500
chunk_overlap = 50
```

---

# 22. 长期记忆链路

每次对话先保存 Message。

然后：

```text
Message 总数 % 5 == 0 ?
        │
        ├─ no → 结束
        │
        └─ yes
             ↓
         update_memory(friend)
             ↓
  SystemPrompt(title='记忆')
             +
      原 Friend.memory
             +
       最近 10 条 Message
             ↓
         MemoryGraph
             ↓
             LLM
             ↓
      新的长期记忆摘要
             ↓
       friend.memory
```

---

# 23. MemoryGraph 为什么比 CharGraph 简单？

记忆压缩不需要工具。

所以：

```text
START → agent → END
```

这能帮助新手理解：

> LangGraph 不等于一定要复杂；它只是把流程显式建模。

---

# 24. TTS 并发链路

```text
Django SSE generator
        │
        ▼
     Queue mq
        ▲
        │
 background Thread
        │
   asyncio.run(...)
        │
        ▼
WebSocket connection
   /             \
  /               \
tts_sender      tts_receiver
  │                 │
  │ LLM chunks      │ audio bytes
  ▼                 ▼
TTS service      Base64
  │                 │
  └──────► Queue ◄──┘
              │
              ▼
             SSE
```

---

# 25. 为什么 `Queue` 很重要？

因为两个不同执行世界需要交换数据：

```text
async WebSocket / LangGraph
        ↕
thread-safe Queue
        ↕
sync Django generator
```

Queue 充当中间缓冲层。

---

# 26. SSE 中同时混合文本与音频

消息结构：

```json
{"content": "hello"}
```

或：

```json
{"audio": "BASE64..."}
```

前端根据 key 判断：

```text
content → 加到最后一条 AI message

audio   → 解码 → 播放队列
```

---

# 27. 浏览器音频播放链路

```text
SSE audio Base64
      ↓
atob()
      ↓
Uint8Array
      ↓
audioQueue.push()
      ↓
processQueue()
      ↓
SourceBuffer.appendBuffer()
      ↓
MediaSource
      ↓
Audio element/player
```

`updateend` 再消费下一块，避免 SourceBuffer 同时写入。

---

# 28. ASR 链路

```text
Microphone
   ↓
浏览器录制 PCM
   ↓
FormData audio
   ↓
POST /api/friend/message/asr/asr/
   ↓
ASRView
   ↓
audio.read()
   ↓
3200-byte chunks
   ↓
WebSocket ASR service
   ↓
result-generated events
   ↓
拼 transcription text
   ↓
JSON Response
   ↓
前端把文字作为聊天内容发送
```

---

# 29. 开发模式地址关系

当前前端配置：

```text
Vue:     http://localhost:5173
Django:  http://127.0.0.1:8000
```

所以：

```text
Vue ──跨域请求──► Django
```

Django `settings.py` 使用 CORS 配置允许本地前端。

---

# 30. Django 模板为什么还存在？

虽然开发阶段是 Vue Vite 单独运行，Django 仍有：

```text
index view
re_path fallback
static/frontend
```

说明项目也考虑了把前端 build 后交给 Django/服务器托管的模式。

这也是 `config.js` 中存在：

```text
vue
django
cloud
```

三种平台模式的原因。

---

# 31. 从“教学项目”到“生产项目”还差哪些层？

当前架构适合学习和继续迭代，但生产环境还应该考虑：

```text
配置层
  模型/URL/Key 全部环境化

数据库
  SQLite → PostgreSQL

队列
  长任务 → Celery / Dramatiq / Task Queue

观测
  structured logging / tracing / metrics

AI
  retry / timeout / fallback / model routing

RAG
  metadata / source citation / tenant isolation

安全
  DEBUG=False / SECRET_KEY / ALLOWED_HOSTS / CORS / CSRF

测试
  unit / API / integration / frontend

部署
  Docker / reverse proxy / HTTPS
```

---

# 32. 一条消息的最终“全景图”

```text
[1] User types message
        ↓
[2] InputField.vue
        ↓
[3] streamApi.js
        ↓ JWT
[4] POST /api/friend/message/chat/
        ↓
[5] web/urls.py
        ↓
[6] MessageChatView
        ↓
[7] authenticate + validate friend
        ↓
[8] build SystemMessage
        ↓
[9] load recent Message rows
        ↓
[10] CharGraph.create_app()
        ↓
[11] agent LLM
        ↓
[12] tool call?
        ├───────── no ──────┐
        │                   │
        └ yes               │
          ↓                 │
[13] ToolNode               │
      ├─ get_time           │
      └─ LanceDB RAG        │
          ↓                 │
[14] agent again ◄──────────┘
        ↓
[15] astream message chunks
        ↓
[16] TTS WebSocket sender
        ↓
[17] Queue content
        │
        ├───────────────► SSE content
        │
[18] TTS audio bytes
        ↓
[19] Base64
        ↓
[20] Queue audio
        ↓
[21] SSE audio
        ↓
[22] browser
      ├─ append text
      └─ MediaSource play audio
        ↓
[23] save Message
        ↓
[24] every 5 messages
        ↓
[25] update_memory()
        ↓
[26] Friend.memory updated
```

如果你能把这张图解释给别人听，你已经真正掌握 AiFriends 的核心架构。
