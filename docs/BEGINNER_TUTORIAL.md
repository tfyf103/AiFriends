# AiFriends：从 0 开始完整复刻教程

> 这不是“把命令抄一遍”的安装文档，而是一套边复刻项目、边学习 **Vue 3 + Django + REST API + JWT + LangChain + LangGraph + RAG + SSE + ASR/TTS** 的入门课程。

如果你此前只会一点 Python，甚至没有做过完整 Web 项目，也可以按顺序学习。

---

# 0. 先认识：我们到底要做什么？

AiFriends 是一个前后端分离的 AI 角色陪伴应用。

用户可以：

1. 注册 / 登录；
2. 创建 AI 角色；
3. 设置角色头像、背景、人格和声音；
4. 把角色添加为好友；
5. 与角色进行文本对话；
6. 接收 LLM 流式回复；
7. 使用工具调用；
8. 使用知识库 RAG；
9. 保存最近聊天和长期记忆；
10. 使用麦克风进行语音输入；
11. 边生成文本边播放 AI 语音。

从架构上看：

```text
浏览器
  │
  │ Vue 3
  ▼
Frontend
  │
  │ HTTP / SSE
  ▼
Django REST Framework
  │
  ├──────────────► SQLite
  │
  ├──────────────► LangGraph / LangChain
  │                   │
  │                   ├──► LLM
  │                   └──► Tools
  │                           ├── 时间工具
  │                           └── LanceDB RAG
  │
  └──────────────► WebSocket 语音服务
                      ├── ASR
                      └── TTS
```

---

# 1. 新手必须先懂的 12 个词

## 1.1 前端

运行在浏览器里的代码。

本项目使用 Vue 3。

前端负责：

- 页面；
- 按钮；
- 输入框；
- 路由；
- 用户状态；
- 调后端 API；
- 把流式 AI 回复显示出来；
- 播放语音。

---

## 1.2 后端

运行在服务器上的代码。

本项目使用 Django + Django REST Framework。

后端负责：

- 注册登录；
- 数据库；
- 角色 CRUD；
- 好友关系；
- 聊天记录；
- 调用 LLM；
- LangGraph Agent；
- RAG；
- 长期记忆；
- ASR / TTS。

---

## 1.3 API

API 可以先粗暴理解成：

> 前端和后端约定好的“通信地址 + 数据格式”。

例如：

```text
POST /api/friend/message/chat/
```

前端发送：

```json
{
  "friend_id": 12,
  "message": "你好"
}
```

后端收到后开始生成 AI 回复。

---

## 1.4 HTTP

浏览器与服务器通信的一套规则。

常见方法：

```text
GET     读取
POST    创建 / 执行动作
PUT     整体更新
PATCH   局部更新
DELETE  删除
```

本项目大量使用 POST。

---

## 1.5 JSON

前后端经常用 JSON 传数据：

```json
{
  "username": "alice",
  "profile": "hello"
}
```

它很像 Python 字典，也很像 JavaScript 对象。

---

## 1.6 JWT

JWT 是一种身份认证方式。

可以把 access token 理解成“短期通行证”。

```text
登录
 ↓
获得 access token
 ↓
请求 API 时带上
Authorization: Bearer xxxxx
```

access token 过期后，再用 refresh token 换新的。

---

## 1.7 SSE

Server-Sent Events。

普通请求通常是：

```text
请求 ───────────────► 后端
请求 ◄─────────────── 完整结果
```

但 LLM 一次回答可能要几秒。

SSE 可以：

```text
你好
你好，
你好，我
你好，我是
你好，我是你的
...
```

后端不断向浏览器推送小片段。

本项目的 AI 文字和 TTS 音频都通过 SSE 返回。

---

## 1.8 LLM

Large Language Model，大语言模型。

本项目使用 OpenAI-compatible 接口形式调用模型。

也就是说代码使用 `ChatOpenAI`，但底层服务不一定非得是 OpenAI 官方接口；关键是服务商是否提供兼容接口。

---

## 1.9 LangChain

LangChain 在本项目里主要帮助我们：

- 用统一 Message 对象组织对话；
- 定义 Tool；
- 对接模型；
- 对接向量数据库；
- 对接 Embedding。

---

## 1.10 LangGraph

LangGraph 用“图”编排 AI 工作流。

本项目的核心循环：

```text
START
  ↓
agent
  │
  ├─ 不需要工具 ─────► END
  │
  └─ 需要工具
       ↓
     tools
       ↓
     agent
       ↓
      ...
```

---

## 1.11 RAG

Retrieval-Augmented Generation，检索增强生成。

一句话理解：

> 先从自己的资料里找相关内容，再让 LLM 根据资料回答。

---

## 1.12 Embedding

Embedding 会把文本转换为一个高维数字向量。

例如：

```text
“猫喜欢吃鱼”
    ↓
[0.014, -0.281, 0.933, ...]
```

语义相近的文本，其向量通常也更接近。

所以可以做“语义搜索”。

---

# 2. 准备开发环境

## 2.1 安装 Git

验证：

```bash
git --version
```

能显示版本即可。

---

## 2.2 安装 Python

本项目当前固定：

```text
Django==6.0.5
```

Django 6.0 支持 Python 3.12、3.13、3.14。

对新手推荐：

```text
Python 3.12.x 或 Python 3.13.x
```

验证：

```bash
python --version
```

Windows 某些机器需要：

```bash
py --version
```

---

## 2.3 安装 Node.js

当前 `frontend/package.json` 要求：

```text
Node ^20.19.0 或 >=22.12.0
```

验证：

```bash
node -v
npm -v
```

---

## 2.4 推荐安装 VS Code

推荐扩展：

- Python
- Vue - Official
- GitLens（可选）

---

# 3. 克隆代码

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

此时目录大致分成：

```text
AiFriends/
├── backend/        # Django
├── frontend/       # Vue
├── docs/           # 教程
├── requirements.txt
├── .env.example
└── README.md
```

最重要的原则：

> `backend` 和 `frontend` 是两个可以分别运行的程序。

---

# 4. 创建 Python 虚拟环境

为什么需要虚拟环境？

假设：

```text
项目 A 需要 Django 5
项目 B 需要 Django 6
```

如果所有包都装到系统 Python，会互相污染。

虚拟环境就是给每个项目单独准备依赖空间。

---

## 4.1 创建环境

在项目根目录：

```bash
python -m venv .venv
```

---

## 4.2 Windows 激活

PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD：

```cmd
.venv\Scripts\activate.bat
```

---

## 4.3 macOS / Linux 激活

```bash
source .venv/bin/activate
```

激活后一般能看到：

```text
(.venv)
```

---

# 5. 安装后端依赖

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

验证：

```bash
python -c "import django; print(django.get_version())"
```

应该看到：

```text
6.0.5
```

再验证 LangChain：

```bash
python -c "import langchain; print(langchain.__version__)"
```

---

# 6. 配置 `.env`

项目已经提供：

```text
.env.example
```

复制：

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

打开 `.env`：

```env
API_KEY=your_api_key_here
API_BASE=https://your-openai-compatible-endpoint/v1
WSS_URL=wss://your-speech-service-websocket-endpoint
```

## 6.1 `API_KEY`

当前这些模块会用到：

```text
ChatOpenAI
OpenAI Embeddings
ASR
TTS
```

## 6.2 `API_BASE`

用于 OpenAI-compatible HTTP API。

当前模型代码在：

```text
backend/web/views/friend/message/chat/graph.py
backend/web/views/friend/message/memory/graph.py
backend/web/documents/utils/custom_embeddings.py
```

## 6.3 `WSS_URL`

用于语音 WebSocket 服务。

相关代码：

```text
backend/web/views/friend/message/asr/asr.py
backend/web/views/friend/message/chat/chat.py
```

## 6.4 为什么不要提交 `.env`？

因为里面有 API Key。

API Key 相当于“云服务银行卡密码”。

永远不要写到：

- GitHub README；
- issue；
- 截图；
- 前端 JavaScript；
- public 仓库。

---

# 7. 第一次启动 Django

进入后端：

```bash
cd backend
```

---

## 7.1 理解 `manage.py`

`manage.py` 是 Django 项目的命令入口。

常见命令：

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

---

## 7.2 数据库迁移

执行：

```bash
python manage.py migrate
```

SQLite 数据库会创建在：

```text
backend/db.sqlite3
```

新手可以把 SQLite 暂时理解成：

> 一个数据库被装进了单个文件里。

因此不用先安装 MySQL / PostgreSQL。

---

## 7.3 启动服务器

```bash
python manage.py runserver
```

默认：

```text
http://127.0.0.1:8000
```

看到：

```text
Starting development server at http://127.0.0.1:8000/
```

说明 Django 已经跑起来。

这个终端不要关。

---

# 8. 启动 Vue 前端

新开第二个终端。

进入：

```bash
cd AiFriends/frontend
```

安装依赖：

```bash
npm install
```

启动：

```bash
npm run dev
```

一般显示：

```text
http://localhost:5173
```

打开浏览器访问它。

---

# 9. 为什么前端知道后端在哪里？

看：

```text
frontend/src/js/config/config.js
```

当前本地开发模式：

```js
const platform = 'vue'
```

因此：

```text
HTTP_URL = http://127.0.0.1:8000
VAD_URL  = http://localhost:5173/vad/
```

也就是说：

```text
浏览器页面       localhost:5173
后端 API         127.0.0.1:8000
```

这是典型的前后端分离开发方式。

---

# 10. CORS 是什么？

浏览器发现：

```text
前端 localhost:5173
后端 127.0.0.1:8000
```

它们不是同一个 Origin。

浏览器会进行跨域安全检查。

Django 配置位于：

```text
backend/backend/settings.py
```

项目使用：

```python
django-cors-headers
```

并允许：

```text
http://localhost:5173
```

如果你把 Vite 改成别的端口，需要同步修改 CORS。

---

# 11. Vue 是怎么启动的？

入口：

```text
frontend/src/main.js
```

核心逻辑：

```js
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

逐句理解：

## 11.1 `createApp(App)`

创建 Vue 应用。

## 11.2 `createPinia()`

注册全局状态管理。

## 11.3 `app.use(router)`

注册路由。

## 11.4 `mount('#app')`

把 Vue 页面挂到 HTML：

```html
<div id="app"></div>
```

---

# 12. Vue Router：为什么 URL 改了页面也会改？

文件：

```text
frontend/src/router/index.js
```

路由类似一个表：

```text
/                         → HomepageIndex
/friend                   → FriendIndex
/create                   → CreateIndex
/user/account/login       → LoginIndex
/user/account/register    → RegisterIndex
```

例如浏览器进入：

```text
/friend
```

Vue Router 就显示：

```text
FriendIndex.vue
```

---

# 13. 路由守卫：为什么未登录不能进入某些页面？

路由里有：

```js
meta: {
  needLogin: true,
}
```

然后：

```js
router.beforeEach(...)
```

进入页面前先判断：

```text
这个页面要登录吗？
      ↓ 是
用户登录了吗？
      ↓ 否
跳转登录页
```

这就是“前端路由守卫”。

注意：

> 前端路由守卫不是安全边界。

真正的安全仍然要由后端：

```python
permission_classes = [IsAuthenticated]
```

保证。

---

# 14. Pinia：用户登录状态放在哪里？

文件：

```text
frontend/src/stores/user.js
```

里面保存：

```text
id
username
photo
profile
accessToken
hasPulledUserInfo
```

为什么不能让每个页面自己保存？

因为：

```text
导航栏要知道用户是谁
个人主页要知道用户是谁
API 要拿 access token
路由守卫要判断登录状态
```

它们都需要共享状态。

所以使用 Pinia。

---

# 15. Axios：普通 API 请求怎么发？

文件：

```text
frontend/src/js/http/api.js
```

创建 Axios 实例：

```js
const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
})
```

之后页面只需要：

```js
api.post('/api/xxx/', data)
```

---

# 16. 为什么 Axios 要做拦截器？

每个需要登录的请求都要带：

```http
Authorization: Bearer <access_token>
```

如果每个组件手写，会重复几十遍。

因此统一：

```js
api.interceptors.request.use(...)
```

自动加 header。

---

# 17. Access Token 过期怎么办？

`api.js` 的 response interceptor 会判断：

```text
HTTP 401
  ↓
access token 可能过期
  ↓
请求 refresh_token API
  ↓
拿到新的 access token
  ↓
重新发送刚才失败的请求
```

而且代码还处理了多个请求同时 401 的情况：

```text
isRefreshing
refreshSubscribers
```

这是一个非常值得学习的真实工程问题：

> 不要让 10 个失败请求同时刷新 10 次 token。

---

# 18. Django URL 是后端总目录

看：

```text
backend/web/urls.py
```

它把 URL 映射到 View。

例如：

```python
path('api/friend/message/chat/', MessageChatView.as_view())
```

可以读成人话：

> 收到 `/api/friend/message/chat/` 请求时，交给 `MessageChatView`。

当前后端 API 包括：

```text
用户
/api/user/account/login/
/api/user/account/logout/
/api/user/account/register/
/api/user/account/refresh_token/
/api/user/account/get_user_info/
/api/user/profile/update/

角色
/api/create/character/create/
/api/create/character/update/
/api/create/character/remove/
/api/create/character/get_single/
/api/create/character/get_list/
/api/create/character/voice/get_list/

首页
/api/homepage/index/

好友
/api/friend/get_or_create/
/api/friend/remove/
/api/friend/get_list/

聊天
/api/friend/message/chat/
/api/friend/message/get_history/

语音识别
/api/friend/message/asr/asr/
```

---

# 19. Django Model：Python 类为什么能变成数据库表？

看：

```text
backend/web/models/friend.py
```

例如：

```python
class Friend(models.Model):
    ...
```

Django ORM 会把它映射成数据库表。

当前核心关系：

```text
User
 ↓ 1:1
UserProfile
 ↓
Character
 ↓
Friend
 ↓
Message
```

另外还有：

```text
Voice
SystemPrompt
```

---

# 20. Friend 为什么有 `memory`？

```python
memory = models.TextField(...)
```

这里保存的是“压缩后的长期记忆”。

不是保存所有对话。

聊天原文保存在：

```python
Message
```

因此：

```text
Message = 原始历史
Friend.memory = 长期摘要
```

---

# 21. Message 为什么保存 token 数？

```text
input_tokens
output_tokens
total_tokens
```

这些字段能帮助你未来做：

- 成本统计；
- 用户额度；
- 模型调用分析；
- prompt 优化；
- 上下文长度控制。

这是从 Demo 走向产品时非常重要的数据。

---

# 22. 第一次创建 Django Admin

进入：

```bash
cd backend
```

执行：

```bash
python manage.py createsuperuser
```

按提示创建管理员。

然后访问：

```text
http://127.0.0.1:8000/admin/
```

本项目 Admin 已注册：

```text
UserProfile
Character
Voice
Friend
Message
SystemPrompt
```

---

# 23. 为什么新手建议先在 Admin 配置 Voice？

`Character.voice` 指向：

```python
Voice
```

Voice 有：

```text
name
voice_id
```

其中 `voice_id` 必须是你的 TTS 服务支持的真实音色 ID。

如果没配置 Voice，文本聊天可以先调试，但 TTS 相关代码需要注意空值。

推荐第一次学习时分两阶段：

```text
阶段 A：先跑通纯文本聊天
阶段 B：再配置 ASR / TTS
```

---

# 24. SystemPrompt 是什么？

模型：

```text
SystemPrompt
```

字段：

```text
title
order_number
prompt
```

项目使用两类 title：

```text
回复
记忆
```

## 24.1 `回复`

用于普通聊天系统提示词。

## 24.2 `记忆`

用于“把近期对话压缩成长期记忆”。

你可以在 Admin 添加：

```text
title: 回复
order_number: 1
prompt: 你需要始终保持角色设定，回答自然，不要说明自己正在扮演角色。
```

再添加：

```text
title: 记忆
order_number: 1
prompt: 请根据原始记忆和最近对话，生成简洁、稳定、可长期使用的用户相关记忆。不要虚构事实。
```

这些只是学习示例。实际项目应继续迭代提示词。

---

# 25. 进入整个项目最核心的聊天链路

前端文件：

```text
frontend/src/components/character/chat_field/input_field/InputField.vue
```

用户输入：

```text
你好
```

点击发送后：

```js
streamApi('/api/friend/message/chat/', {
  body: {
    friend_id: props.friendId,
    message: content,
  }
})
```

因此发到后端：

```text
POST /api/friend/message/chat/
```

---

# 26. 为什么聊天不用普通 Axios？

因为普通 JSON Response 通常要等完整答案。

但我们想要：

```text
第 1 个 token 来了 → 页面立即显示
第 2 个 token 来了 → 页面继续显示
第 3 个 token 来了 → 页面继续显示
```

所以使用 SSE。

前端专门有：

```text
frontend/src/js/http/streamApi.js
```

它使用：

```text
@microsoft/fetch-event-source
```

---

# 27. SSE 消息长什么样？

后端会生成：

```text
data: {"content":"你"}

```

然后：

```text
data: {"content":"好"}

```

音频则可能是：

```text
data: {"audio":"BASE64..."}

```

结束：

```text
data: [DONE]

```

前端 `streamApi.js` 负责解析。

---

# 28. 后端聊天入口 `MessageChatView`

文件：

```text
backend/web/views/friend/message/chat/chat.py
```

请求首先：

```python
permission_classes = [IsAuthenticated]
```

说明必须登录。

然后取：

```text
friend_id
message
```

接着验证：

```text
消息是不是空？
好友存在吗？
这个好友属于当前登录用户吗？
```

这是非常重要的后端原则：

> 永远不要相信前端传来的 ID。

即使前端隐藏按钮，攻击者仍然能自己构造 HTTP 请求。

---

# 29. 为什么要加 System Prompt？

`add_system_prompt()` 会拼：

```text
数据库里的“回复”提示词
+
角色性格 friend.character.profile
+
长期记忆 friend.memory
```

最终大致：

```text
[系统规则]
...

[角色性格]
温柔、理性、喜欢摄影...

[长期记忆]
用户正在学习 Python...
```

这就是角色“人设”与“记忆”的来源。

---

# 30. 为什么还要加最近聊天？

`add_recent_messages()` 会取最近：

```python
Message.objects.filter(friend=friend).order_by('-id')[:10]
```

再变成：

```text
HumanMessage
AIMessage
HumanMessage
AIMessage
...
```

所以当前 prompt 大致包含：

```text
系统提示词
长期记忆
最近 10 条数据库对话
当前问题
```

这样模型才知道“我们刚才聊了什么”。

---

# 31. LangChain Message 为什么比字符串好？

模型不是只看到一大段文本，而是有角色结构：

```text
SystemMessage
HumanMessage
AIMessage
ToolMessage
```

它们分别表示：

```text
SystemMessage  系统规则
HumanMessage   用户
AIMessage      AI
ToolMessage    工具执行结果
```

这就是现代 Chat API 的基本结构。

---

# 32. `CharGraph.create_app()`：LangGraph 核心

文件：

```text
backend/web/views/friend/message/chat/graph.py
```

当前图中有两个节点：

```text
agent
tools
```

---

# 33. 第一个 Tool：`get_time`

```python
@tool
def get_time() -> str:
    ...
```

函数本身并不复杂。

真正关键的是：

```python
@tool
```

它把普通 Python 函数转换成模型可调用工具。

模型可以根据：

- 函数名；
- 参数；
- docstring；

决定是否调用。

所以 Tool 的 docstring 非常重要。

---

# 34. 第二个 Tool：知识库搜索

```python
@tool
def search_knowledge_base(query: str) -> str:
```

它连接：

```text
./web/documents/lancedb_storage
```

然后：

```python
similarity_search(query, k=3)
```

找到最相关的 3 个文档块。

---

# 35. `bind_tools(tools)` 是什么？

```python
ChatOpenAI(...).bind_tools(tools)
```

相当于告诉模型：

> 除了直接说话，你还可以使用这些函数。

模型并不会自己执行 Python。

它只会产生类似：

```text
我要调用 search_knowledge_base
参数 query="..."
```

真正执行工具的是 LangGraph 的：

```python
ToolNode(tools)
```

---

# 36. `StateGraph` 是什么？

状态：

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

你可以先理解为：

```text
整个 Agent 在运行过程中，共享一个 messages 列表。
```

每走一个节点，都可以读取 / 添加 message。

---

# 37. `model_call()` 做什么？

```python
res = llm.invoke(state['messages'])
```

即：

> 把当前完整消息上下文发给模型。

模型可能：

1. 直接回复；
2. 要求调用工具。

---

# 38. `should_continue()` 做什么？

它看最后一条 AI Message：

```python
if last_message.tool_calls:
    return "tools"
return "end"
```

所以：

```text
模型有 tool_calls
    ↓
tools

没有
    ↓
END
```

---

# 39. 为什么 Tools 后还要回 Agent？

工具只负责查数据。

例如：

```text
用户：阿里云百炼的某功能是什么？
```

模型：

```text
需要搜索知识库
```

Tool：

```text
返回 3 个资料片段
```

但资料片段还不是自然语言最终回答。

所以：

```text
tools → agent
```

让模型读完 Tool 结果后再生成答案。

---

# 40. 这就是一个最小 Agent Loop

完整逻辑：

```text
START
  ↓
agent
  ↓
是否 tool_call？
  ├─ 否 → END
  └─ 是 → tools
            ↓
          agent
            ↓
          再判断
```

如果你能理解这一节，就已经理解了 LangGraph 最核心的思想。

---

# 41. 为什么要流式 `astream()`？

聊天 View 里：

```python
app.astream(inputs, stream_mode="messages")
```

这样不需要等完整 AIMessage 生成后再返回。

而是模型一边生成：

```text
chunk 1
chunk 2
chunk 3
```

后端一边处理。

---

# 42. 文本为什么能一边生成一边变成语音？

这是本项目很有意思的一部分。

`tts_sender()`：

```text
LangGraph 流式 token
    ↓
每来一个文本 chunk
    ↓
发给 TTS WebSocket
```

同时：

```text
文本 chunk
    ↓
Queue
    ↓
SSE
    ↓
浏览器显示文字
```

另一边 `tts_receiver()`：

```text
TTS 音频二进制
    ↓
Base64
    ↓
Queue
    ↓
SSE
    ↓
浏览器播放
```

因此文本和声音可以近似并行。

---

# 43. 为什么后端要线程 + asyncio + Queue？

当前聊天链路同时涉及：

- Django 同步 View；
- LangGraph async stream；
- WebSocket async；
- SSE generator；
- TTS 双工通信。

所以代码使用：

```text
threading.Thread
asyncio.run
asyncio.gather
Queue
```

可以先理解为：

```text
一个后台线程专门处理异步 LLM + TTS

主 SSE generator 不断从 Queue 取：
  content
  audio
  usage
```

这部分属于进阶 Python 并发知识。

第一次学习时不必一次全掌握。

---

# 44. AI 回复最后怎么落库？

流结束后：

```python
Message.objects.create(...)
```

保存：

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
```

所以刷新页面后，还能从数据库加载聊天历史。

---

# 45. 长期记忆为什么每 5 轮更新？

当前代码：

```python
if Message.objects.filter(friend=friend).count() % 5 == 0:
    update_memory(friend)
```

意思是每累计 5 条 Message，重新压缩一次长期记忆。

为什么不每次都做？

因为记忆更新本身也要调用 LLM：

```text
更多延迟
更多 token
更多成本
```

为什么也不能永远不更新？

因为角色会“忘记”更早发生的事情。

因此这是成本、速度和记忆质量之间的折中。

---

# 46. `update_memory()` 怎么工作？

文件：

```text
backend/web/views/friend/message/memory/update.py
```

构造：

```text
SystemMessage：记忆更新规则
HumanMessage：原始长期记忆 + 最近对话
```

然后调用：

```text
MemoryGraph
```

最终：

```python
friend.memory = res['messages'][-1].content
friend.save()
```

---

# 47. 这是一种“压缩记忆”设计

假设完整聊天有：

```text
1000 条消息
```

每次都全部放进 prompt：

```text
慢
贵
上下文可能超限
噪声大
```

所以：

```text
原始消息保存在数据库
        ↓
最近少量消息直接使用
        ↓
历史信息压缩成长期记忆
```

这是很多长期 Agent 系统都会采用的基本思路之一。

---

# 48. RAG 第一阶段：准备原始文档

项目默认把知识库原始内容放到：

```text
backend/web/documents/data.txt
```

这个文件被 `.gitignore` 忽略。

所以第一次复刻时需要自己创建：

```text
backend/web/documents/data.txt
```

放一段你自己的测试知识，例如：

```text
AiFriends 是一个使用 Vue 3、Django、LangChain 与 LangGraph 构建的 AI 伙伴项目。

AiFriends 使用 LanceDB 保存向量化后的知识库文本块。
```

---

# 49. RAG 第二阶段：TextLoader

`insert_documents.py`：

```python
loader = TextLoader(...)
documents = loader.load()
```

原始 txt 变成 LangChain Document。

---

# 50. RAG 第三阶段：切块

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

为什么不能把一本书整个 Embedding？

因为：

- 语义太杂；
- 检索粒度太粗；
- 模型上下文浪费；
- Embedding API 也有长度限制。

所以切成小块。

`chunk_overlap=50` 表示相邻片段有部分重叠，降低“关键信息正好被切断”的风险。

---

# 51. RAG 第四阶段：Embedding

文件：

```text
backend/web/documents/utils/custom_embeddings.py
```

实现：

```text
embed_documents(texts)
embed_query(text)
```

也就是说同一套 Embedding 逻辑既能：

- 把知识库文本变向量；
- 把用户问题变向量。

---

# 52. RAG 第五阶段：LanceDB

```python
db = lancedb.connect('./web/documents/lancedb_storage')
```

然后：

```python
LanceDB.from_documents(...)
```

会建立向量数据。

生成目录：

```text
backend/web/documents/lancedb_storage
```

它也被 `.gitignore` 忽略。

原因：

> 向量库通常属于运行时生成数据，不应该直接提交到源码仓库。

---

# 53. 怎么第一次构建知识库？

进入：

```bash
cd backend
python manage.py shell
```

执行：

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

完成后退出：

```python
exit()
```

然后检查：

```text
backend/web/documents/lancedb_storage
```

是否出现数据。

---

# 54. 查询时发生什么？

当模型决定调用：

```text
search_knowledge_base
```

工具做：

```python
vector_db.similarity_search(query, k=3)
```

得到：

```text
最相关片段 1
最相关片段 2
最相关片段 3
```

再交给 LLM。

---

# 55. 注意：当前知识库 Tool 的描述比较专用

当前 docstring 描述的是：

```text
当用户查询阿里云百炼平台的相关信息时...
```

如果你把 AiFriends 改成自己的通用知识库项目，建议同步把 Tool 描述改成你的领域。

否则模型可能认为：

> 只有问阿里云百炼时才能使用这个 Tool。

Tool 描述本身就是 Agent 行为设计的一部分。

---

# 56. ASR：语音怎么变成文字？

后端：

```text
backend/web/views/friend/message/asr/asr.py
```

API：

```text
POST /api/friend/message/asr/asr/
```

浏览器上传：

```text
audio
```

后端读取 PCM：

```python
pcm_data = audio.read()
```

然后建立 WebSocket，分片发送音频。

---

# 57. 为什么 ASR 要分片？

代码：

```python
chunk = 3200
```

不是一次把全部音频扔过去。

而是：

```text
3200 bytes
3200 bytes
3200 bytes
...
```

更接近实时流式语音识别。

---

# 58. TTS：文字怎么变成声音？

聊天生成 token 的同时：

```text
文本 chunk
  ↓
WebSocket TTS
  ↓
mp3 bytes
```

后端再：

```python
base64.b64encode(msg)
```

为什么要 Base64？

因为 SSE 主要传文本。

所以把二进制音频编码成字符串再发送。

---

# 59. 前端怎么播放“不断到达”的 MP3？

文件：

```text
InputField.vue
```

使用浏览器：

```text
MediaSource
SourceBuffer
Audio
```

流程：

```text
Base64
 ↓ atob
binary string
 ↓
Uint8Array
 ↓
audioQueue
 ↓
SourceBuffer.appendBuffer()
 ↓
Audio 播放
```

这样就不需要等完整 mp3 文件生成后才播放。

---

# 60. 为什么要 `audioQueue`？

`SourceBuffer` 正在更新时不能随便再次写入。

所以：

```text
音频片段不断到来
      ↓
先放 audioQueue
      ↓
当前 append 完成
      ↓
updateend
      ↓
继续 processQueue()
```

这是典型的“生产者 / 消费者”思想。

---

# 61. 第一次复刻时建议关闭哪些复杂功能？

如果你完全是新手，不要一上来同时调 8 个系统。

建议按阶段：

## Stage A：前后端基本页面

目标：

```text
Vue + Django 都能启动
```

## Stage B：用户认证

目标：

```text
注册 / 登录 / Token 刷新
```

## Stage C：角色与好友

目标：

```text
Character CRUD + Friend
```

## Stage D：纯文本 LLM

临时只做：

```text
用户 → LLM → 完整文本
```

## Stage E：SSE

变成：

```text
用户 → LLM → 流式文本
```

## Stage F：LangGraph + Tool

先只留：

```text
get_time
```

## Stage G：长期记忆

加入：

```text
Friend.memory
```

## Stage H：RAG

加入：

```text
Embedding + LanceDB
```

## Stage I：ASR

加入麦克风。

## Stage J：TTS

最后再加边生成边播放。

---

# 62. 真正学习前端：建议自己重写哪些组件？

不要一开始重写整个项目。

按顺序自己实现：

```text
1. 一个按钮
2. 一个输入框 v-model
3. 一个消息数组 v-for
4. 父子组件 props
5. 子组件 emit
6. Vue Router 两个页面
7. Pinia 保存 username
8. Axios 调一个 GET/POST
9. 登录表单
10. 聊天输入框
11. SSE 流式输出
12. 音频队列
```

---

# 63. 真正学习后端：建议自己重写哪些 API？

顺序：

```text
1. Hello API
2. Model
3. migrate
4. 创建数据
5. 查询数据
6. 用户注册
7. JWT 登录
8. IsAuthenticated
9. Character CRUD
10. Friend
11. Message
12. StreamingHttpResponse
13. LLM
14. LangGraph
15. RAG
```

---

# 64. 真正学习 LangChain：不要从 Agent 开始

建议先在单独 Python 文件理解：

## Step 1

```python
from langchain_openai import ChatOpenAI
```

调用一次模型。

## Step 2

理解：

```python
SystemMessage
HumanMessage
AIMessage
```

## Step 3

定义一个：

```python
@tool
```

## Step 4

理解：

```python
bind_tools
```

## Step 5

再看：

```text
StateGraph
ToolNode
conditional_edges
```

这样难度会低很多。

---

# 65. 浏览器 DevTools 是你的第一调试工具

按 F12。

重点看：

## Console

JavaScript 报错。

## Network

看每个请求：

```text
URL
Method
Status
Request Payload
Response
Headers
```

## Application

看 Cookie / Storage。

---

# 66. Django 终端是你的第二调试工具

后端出现：

```text
500 Internal Server Error
```

不要只看浏览器。

马上看：

```text
python manage.py runserver
```

那个终端里的 traceback。

Python traceback 往往已经告诉你：

```text
哪一个文件
第几行
什么异常
```

---

# 67. 学会判断 HTTP 状态码

常见：

```text
200 成功
201 创建成功
400 请求数据不对
401 未登录 / Token 无效
403 没权限
404 地址或资源不存在
500 后端代码报错
```

看到错误先看状态码，再看 Response。

---

# 68. 最容易出现的启动顺序错误

正确建议：

```text
1. 激活 Python venv
2. Django migrate
3. Django runserver
4. 新终端
5. npm install
6. npm run dev
7. 浏览器
```

如果需要 LLM：

```text
8. 配置 .env
```

如果需要 RAG：

```text
9. 创建 data.txt
10. insert_documents()
```

如果需要语音：

```text
11. 配置 WSS_URL
12. Admin 添加 Voice
```

---

# 69. 一次完整请求，请你自己手动跟踪一遍

在 VS Code 依次打开：

```text
frontend/src/components/character/chat_field/input_field/InputField.vue
frontend/src/js/http/streamApi.js
backend/web/urls.py
backend/web/views/friend/message/chat/chat.py
backend/web/views/friend/message/chat/graph.py
backend/web/models/friend.py
```

然后问自己：

1. 点击发送调用哪个函数？
2. 请求 URL 是什么？
3. Authorization 在哪里加？
4. Django URL 怎么匹配？
5. 后端怎么确认 friend 属于当前用户？
6. SystemPrompt 在哪加？
7. 最近聊天在哪加？
8. LangGraph 在哪创建？
9. Tool 在哪定义？
10. token 怎么变成 SSE？
11. 音频怎么变成 Base64？
12. 前端怎么拼接文本？
13. 前端怎么播放音频？
14. 最终 Message 怎么保存？
15. 长期记忆什么时候更新？

如果你能不用看答案说清楚这 15 个问题，说明已经真正理解项目主干。

---

# 70. 推荐的 18 次 Git 学习提交

如果你要从空项目复刻：

```text
01 chore: create vue project
02 feat: add vue router
03 feat: add login register pages
04 feat: create django project
05 feat: add user models and jwt auth
06 feat: connect frontend auth api
07 feat: add character models and crud
08 feat: add friend relationship
09 feat: add chat ui
10 feat: add message model
11 feat: add basic llm chat
12 feat: add sse streaming
13 feat: add langgraph agent
14 feat: add tool calling
15 feat: add long term memory
16 feat: add lancedb rag
17 feat: add asr
18 feat: add streaming tts
```

这样你随时可以：

```bash
git log --oneline
```

回看自己的成长路径。

---

# 71. 一比一复刻完成检查表

## 环境

- [ ] Git 可用
- [ ] Python 3.12 / 3.13 可用
- [ ] Node 符合 package.json 要求
- [ ] `.venv` 已创建
- [ ] `pip install -r requirements.txt` 成功
- [ ] `npm install` 成功

## Django

- [ ] `migrate` 成功
- [ ] `runserver` 成功
- [ ] `/admin/` 可以打开
- [ ] superuser 可以登录

## Vue

- [ ] `npm run dev` 成功
- [ ] 首页能打开
- [ ] Vue Router 正常

## 用户

- [ ] 注册成功
- [ ] 登录成功
- [ ] access token 生效
- [ ] 页面刷新后能恢复用户状态
- [ ] access token 过期可以刷新

## 角色

- [ ] Voice 已配置
- [ ] 角色创建成功
- [ ] 图片上传成功
- [ ] 角色编辑成功
- [ ] 好友关系成功

## LLM

- [ ] `.env` API_KEY 正确
- [ ] `.env` API_BASE 正确
- [ ] ChatOpenAI 调用成功
- [ ] 普通文本回复成功
- [ ] SSE 流式回复成功
- [ ] token usage 能保存

## LangGraph

- [ ] `get_time` 可调用
- [ ] Agent 能从 tools 回到 agent

## Memory

- [ ] Message 历史保存
- [ ] 最近聊天能进入上下文
- [ ] 每 5 条 Message 更新长期记忆
- [ ] Friend.memory 有内容

## RAG

- [ ] `data.txt` 已创建
- [ ] Embedding API 可用
- [ ] LanceDB 成功创建
- [ ] `similarity_search` 有结果
- [ ] 模型能触发知识库 Tool

## Voice

- [ ] WSS_URL 可用
- [ ] ASR 成功
- [ ] TTS 成功
- [ ] 浏览器能播放连续音频片段

---

# 72. 下一步应该改什么？

当你能完整复刻后，建议按工程价值排序继续做：

1. 把模型名、Embedding 模型名、语音模型名全部移入配置；
2. 把 `platform = 'vue'` 改为 Vite 环境变量；
3. 给聊天、认证、角色 CRUD 加测试；
4. 给 LLM 调用增加 timeout / retry；
5. 给 RAG 增加 metadata 与来源引用；
6. 把知识库 Tool 从“阿里云百炼专用”改为角色级 / 用户级知识库；
7. 给长期记忆增加结构化 schema；
8. 增加模型供应商抽象层；
9. 处理没有 Voice 时的文本-only 模式；
10. 给异步 TTS 线程增加异常向 SSE 的传播；
11. 增加 Docker / docker compose；
12. 从 SQLite 演进到 PostgreSQL；
13. 给 API 增加 OpenAPI / Swagger 文档；
14. 增加 CI；
15. 增加生产环境安全配置。

---

# 73. 最重要的学习原则

不要问：

> “我要多久学会 Vue / Django / LangChain？”

应该问：

> “这一条消息现在运行到哪个文件了？”

当你能从用户点击开始，一层一层追踪数据，你就从“会复制代码”开始变成“会理解系统”。

AiFriends 很适合作为第一套完整 AI 全栈项目，因为它把今天 AI 应用最常见的几条链路放在了同一个仓库：

```text
Vue
Django
JWT
SSE
LLM
Tool Calling
LangGraph
Memory
RAG
Vector DB
ASR
TTS
```

不要试图一天学完。

按链路、按阶段、按 commit 重建一遍，你会学得比单独看十门零散课程更扎实。

---

## 下一篇

继续阅读：

- [系统架构与请求链路](./ARCHITECTURE.md)
- [常见报错与排查手册](./TROUBLESHOOTING.md)
- [学习地图](./README.md)
