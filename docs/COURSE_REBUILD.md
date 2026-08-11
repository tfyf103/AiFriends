# AiFriends 从 0 复刻课程：沿真实 Git 历史学习全栈 + LangChain

> 这套课程不要求你直接啃最终版源码。
>
> 它利用 AiFriends 自己的真实 Git 提交历史，把项目重新拆回最自然的成长顺序：**Vue 页面 → Django → JWT → 角色 CRUD → 好友系统 → 普通聊天 → SSE → LangGraph → 长期记忆 → RAG → ASR → TTS**。
>
> 最终目标不是“看懂这个仓库”，而是：**你能在一个空目录里，自己重新做出一个 AiFriends。**

---

# 0. 为什么要按真实版本学习？

最终版 AiFriends 同时出现：

```text
Vue 3
Vue Router
Pinia
Axios
JWT
Django
DRF
SQLite
SSE
LangChain
LangGraph
Tool Calling
Long-term Memory
Embedding
LanceDB
RAG
ASR
TTS
WebSocket
MediaSource
```

如果第一次学项目就打开最终版 `chat.py`，你会同时看到：

```text
Django
线程
asyncio
Queue
LangGraph
LLM streaming
WebSocket
TTS
SSE
数据库
```

这不是合理的新手学习顺序。

真实项目也不是一天写完的。AiFriends 的历史提交正好展示了一条很自然的工程演进路线：

```text
先有页面
  ↓
再有后端和数据库
  ↓
再有用户身份
  ↓
再有角色和好友业务
  ↓
再接 LLM
  ↓
发现等待太久 → SSE
  ↓
发现模型能力有限 → Tool Calling
  ↓
发现历史越来越长 → Long-term Memory
  ↓
发现模型不知道私有资料 → RAG
  ↓
最后增加 ASR / TTS
```

所以本课程把**真实 commit 当作章节检查点**。

---

# 1. Git 历史怎么用？

## 1.1 查看某个版本改了什么

```bash
git show <commit-sha>
```

例如查看“第一次实现后端流式输出”：

```bash
git show b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

只看文件统计：

```bash
git show --stat b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

---

## 1.2 比较两个阶段

```bash
git diff <旧版本> <新版本>
```

例如比较“普通聊天”和“第一次流式聊天”：

```bash
git diff 72a9866e3370481a8fa6e070e55c7784977c058a b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

这个命令非常适合学习：

> 为了把普通聊天升级成 SSE，到底新增了什么？

---

## 1.3 临时切到历史版本

```bash
git switch --detach <commit-sha>
```

例如：

```bash
git switch --detach 72a9866e3370481a8fa6e070e55c7784977c058a
```

这时出现 `detached HEAD` 是正常的。

如果只是观察代码，没有问题。

---

## 1.4 想从旧版本开始自己写

不要长期在 detached HEAD 上开发。

创建自己的学习分支：

```bash
git switch -c learn/chapter-06 72a9866e3370481a8fa6e070e55c7784977c058a
```

学习结束回教程分支：

```bash
git switch agent/beginner-tutorial
```

或者回主分支：

```bash
git switch main
```

---

# 2. 推荐：另建一个自己的学习仓库

真正想学会，不建议只在 AiFriends 中来回切版本。

新建：

```text
AiFriends-Learning/
```

每完成一个小功能，就 commit：

```bash
git add .
git commit -m "learn: chapter 01 vue router"
```

原项目历史 commit 是“参考答案”。

你的 commit 是“学习轨迹”。

---

# 3. 课程地图

| Chapter | 主题 | 核心技术 | 最终能力 |
|---|---|---|---|
| 00 | 环境与骨架 | Git / Python / Node | 能启动前后端开发环境 |
| 01 | Vue 页面与路由 | Vue / Router | 理解组件和 SPA |
| 02 | Django 与数据库 | Django / ORM / SQLite | 理解 URL → View → Model |
| 03 | 注册登录 | REST / JWT / Pinia / Axios | 打通用户身份链路 |
| 04 | Character CRUD | CRUD / FormData / ImageField | 做完整前后端业务 |
| 05 | 首页与 Friend | ORM Relation / API | 理解业务关系模型 |
| 06 | 普通 AI Chat | LangChain / Messages | 调通一次 LLM 对话 |
| 07 | SSE Streaming | StreamingHttpResponse / SSE | 实现逐段回复 |
| 08 | Agent 与 Tool | LangGraph / ToolNode | 让模型主动调用工具 |
| 09 | Long-term Memory | Summarization / Prompt | 实现压缩式长期记忆 |
| 10 | RAG | Chunk / Embedding / LanceDB | 构建可检索知识库 |
| 11 | ASR | PCM / WebSocket | 声音转文字 |
| 12 | TTS | asyncio / Queue / MediaSource | 边生成边说话 |
| 13 | Full Pipeline | Full Stack AI | 独立追踪整个系统 |

---

# Chapter 00：环境与项目骨架

## 真实检查点

```text
cd5cfb2b387f4fb727cd55f33db36ac3a2a847f7  首次提交：上传本地项目
```

## 学习目标

先只理解：

```text
Git      = 管理代码版本
Python   = 运行 Django 后端
Node.js  = 运行 Vue/Vite 工具链
Browser  = 运行前端 JavaScript
```

## 动手任务

安装：

- Git
- Python
- Node.js
- VS Code

确认版本：

```bash
git --version
python --version
node --version
npm --version
```

创建自己的学习目录：

```text
AiFriends-Learning/
├── backend/
└── frontend/
```

## 本章不要做

不要碰：

```text
LangChain
LangGraph
RAG
向量数据库
语音
```

## 验收

你能解释：

> 为什么 Vue 和 Django 开发时通常需要两个终端？

---

# Chapter 01：Vue 页面、组件与路由

## 真实检查点

```text
e03219b7464ea487f843f7abe74daa98eb7dfd7c  创建导航栏
b1703e8eff39f95dcd8cf3ed7b5d1def0e616758  实现路由
b938159da24699eaec1249251b99ec06884f6b0a  实现登录注册页面
```

## Vue 最小心智模型

```text
main.js
  ↓
createApp(App)
  ↓
App.vue
  ↓
View
  ↓
Component
```

## Router 心智模型

```text
URL
 ↓
Vue Router
 ↓
routes 匹配
 ↓
显示对应 View
```

## 动手任务

先只做前端：

```text
/
/user/account/login
/user/account/register
```

不用 Django。
不用数据库。

## 必须理解

```text
<script setup>
<template>
<style scoped>
```

以及：

```js
ref()
computed()
defineProps()
defineEmits()
```

## 验收

输入不同 URL 时页面切换，但整个浏览器页面不会传统式重新加载。

你能解释：

> View 和 Component 有什么区别？

---

# Chapter 02：Django、ORM 与 SQLite

## 真实检查点

```text
3ab2bd28ca6551e188084e7502de82a06df96b0a  实现完数据库
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  实现后端
```

## Django 四层模型

```text
URL
 ↓
View
 ↓
Model / ORM
 ↓
Database
```

### URL

决定：

> 哪个地址由哪个 View 处理？

### View

决定：

> 收到请求后执行什么业务逻辑？

### Model

决定：

> 数据有哪些字段和关系？

### SQLite

负责真正保存数据。

## 动手任务

创建 Django：

```bash
django-admin startproject backend
python manage.py startapp web
```

学习：

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Migration 心智模型

```text
models.py
   ↓ makemigrations
migration 文件
   ↓ migrate
数据库表
```

## 验收

能打开：

```text
http://127.0.0.1:8000/admin/
```

并且知道 Admin 不是数据库本身，只是 Django 提供的数据库管理界面。

---

# Chapter 03：注册、登录、JWT 与全局用户状态

## 真实检查点

```text
a27cbf8f90cf256ab075173f19d468319b302f67  前端对接注册、登录、退出api
b0aa1d5c169d836023fd3788152d5cb1eb4bf55b  第一次打开页面或刷新页面时，从云端动态拉取用户信息
e2915586d6352180b93500ce8e15dbfa8afa8704  创建更新用户资料后端api
8d06c1ec8c04a70a8a47a1644fd8cd28a63a48e6  实现编辑资料页面前端
```

## 登录完整链路

```text
Login Form
  ↓ POST
Django Login API
  ↓
access token + refresh token
  ↓
Pinia 保存登录状态
  ↓
Axios 自动加 Authorization Header
```

## 为什么有两个 Token？

### access token

短寿命，频繁用于 API 请求。

### refresh token

寿命更长，用于 access token 过期后换新 token。

## 动手任务

后端实现：

```text
register
login
logout
refresh_token
get_user_info
```

前端实现：

```text
Pinia user store
Axios request interceptor
Axios response interceptor
Router guard
```

## 必须亲自调试

打开浏览器 DevTools → Network。

看到：

```text
Authorization: Bearer eyJ...
```

再模拟 access token 过期，理解刷新逻辑。

## 验收

刷新页面后，用户仍然能恢复登录信息，而不是页面刷新一次就“失忆”。

---

# Chapter 04：Character CRUD

## 真实检查点

```text
2081304f049a58a404b39bfe09f9c373b80d24df  实现角色增删改查后端api
1c811b7034f042ed5344efe653e0a31e07c6e00a  给增删改查后端api打补丁
84f1c92eba32c62ef2e5724a77eeb7c64979de6b  实现完创建虚拟角色前端
95cf0456ef46696bca36c602928fbbb6dbe658d5  实现更新虚拟角色前端页面
```

## CRUD

```text
Create
Read
Update
Delete
```

这是 Web 开发最基本的业务闭环。

## Character 数据

```text
Character
├── author
├── name
├── photo
├── background_image
├── profile
└── voice
```

## 新知识：文件上传

普通 JSON 适合：

```json
{"name":"Alice"}
```

图片需要理解：

```text
FormData
multipart/form-data
ImageField
MEDIA_ROOT
MEDIA_URL
```

## 动手任务

完成：

- 创建角色
- 查询角色
- 修改角色
- 删除角色
- 上传头像
- 上传背景图

## 验收

完整追踪：

```text
Vue Form
 ↓
HTTP Request
 ↓
Django View
 ↓
Character Model
 ↓
SQLite + media/
 ↓
GET API
 ↓
Vue Display
```

---

# Chapter 05：首页、搜索、好友关系与聊天框

## 真实检查点

```text
f96da725bbfd77aa9766f70786a6061f35f8dcb9  实现首页前后端
c9ea5e0f3b1a276c3fe6d0b10fa648db3f5510ca  实现搜索功能
102b31a0f60be51bbc6f22f690ec74d3ee0a5be3  实现好友页面后端
fb1394362c3ba60bee544bf8737bca5051ea9ae8  实现聊天框
1c9d9e000c77c4e1779e0681ae5fca7e8123dc67  实现好友列表前端
```

## 关系模型

```text
UserProfile
    |
    | me
    v
Friend
    |
    | character
    v
Character
```

`Friend` 不是另一个真人账号。

它表达：

> 当前用户与某个 AI Character 建立了一条好友/聊天关系。

## 动手任务

实现：

- 首页角色列表
- 搜索角色
- 添加好友
- 好友列表
- 删除好友
- 打开聊天弹窗

## 必须理解 Django ORM

例如：

```python
Friend.objects.filter(me__user=request.user)
```

需要能解释双下划线 `__` 如何跨 ForeignKey 查询。

## 验收

不同用户登录后，只能看到自己的 Friend 关系。

---

# Chapter 06：先做最普通的 AI Chat

## 真实检查点

```text
c82553f13badf75ba372f1bc343b0d14b0bc5081  创建消息数据库
72a9866e3370481a8fa6e070e55c7784977c058a  实现聊天后端
```

## 本章原则

暂时不要：

```text
SSE
LangGraph Tool
Memory
RAG
TTS
```

先实现：

```text
用户消息
  ↓ POST
Django
  ↓
LLM
  ↓
完整文本
  ↓ JSON
Vue
```

## LangChain 只学最少概念

```text
HumanMessage
SystemMessage
AIMessage
ChatOpenAI
invoke()
```

## Message Model

理解为什么要保存：

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
create_time
```

## 动手任务

输入：

```text
你好
```

后端调用模型，等模型完整生成后一次性返回 JSON。

## 验收

聊天可以工作，但你能明显感觉到：

> 模型没生成完之前，页面一直没有回复。

这个体验问题就是下一章引入 SSE 的原因。

---

# Chapter 07：SSE 流式聊天

## 真实检查点

```text
b9ea1c3404b04413d638067de78c3ed4d7262fc3  实现文字交流的后端流式输出
3c7c464b51dcbb411ad50bafe58ad214ecc6eb2c  改造成流式前端回复
031f03137cf8abb5128c3de93bc6f353b93965cf  实现聊天记录的后端
ea419695f4d8e9e2cec97c4f92a03dc7d679e4df  实现聊天记录的流式加载（前后端）
7ba85a3b629a9fdb41307fb6427960ffe674c2b9  流式加载每次返回10条消息
```

## 普通 HTTP

```text
Request
  ↓
等待完整结果
  ↓
Response
```

## SSE

```text
Request
  ↓
data chunk 1
  ↓
data chunk 2
  ↓
data chunk 3
  ↓
[DONE]
```

## SSE 最小协议

```text
data: {"content":"你"}


data: {"content":"好"}


data: [DONE]

```

## 后端重点

```python
StreamingHttpResponse
```

以及生成器：

```python
yield "data: ...\n\n"
```

## 前端重点

```text
fetchEventSource
onopen
onmessage
onerror
```

教学化源码：

```text
frontend/src/js/http/streamApi.js
frontend/src/components/character/chat_field/input_field/InputField.vue
backend/web/views/friend/message/chat/chat.py
```

## 动手任务

先只流式文字，不做语音。

让 AI 气泡：

```text
空字符串
 ↓
追加 chunk 1
 ↓
追加 chunk 2
 ↓
追加 chunk 3
```

## 验收

DevTools → Network 中能看到长连接，页面逐段增长。

---

# Chapter 08：System Prompt、多轮上下文与 LangGraph Tool Calling

## 真实检查点

```text
3bcc4a8c8e169475af6c78b2ac19752b62625bdf  添加系统提示词和多轮记忆对话
72c4c3ae5efb950e7b4f08cded3a37238e961c78  实现function call
```

## 从 LLM 变成 Agent

普通：

```text
messages -> LLM -> answer
```

Agent：

```text
messages
   ↓
agent / LLM
   ↓
需要 Tool？
   ├─ 否 → END
   └─ 是
       ↓
     ToolNode
       ↓
    Tool result
       ↓
     agent
       ↓
    final answer
```

## LangGraph 必学关键词

```text
StateGraph
AgentState
add_messages
Node
Edge
Conditional Edge
START
END
ToolNode
```

## Tool 三层关系

### 1. `@tool`

把普通 Python 函数描述成 Tool。

### 2. `llm.bind_tools(tools)`

把 Tool schema 告诉模型。

它不负责执行函数。

### 3. `ToolNode(tools)`

真正根据 `tool_calls` 执行 Python Tool。

## 第一个 Tool 练习

```python
@tool
def get_time() -> str:
    ...
```

## 当前教学化源码

```text
backend/web/views/friend/message/chat/graph.py
```

## 验收

问：

```text
现在几点？
```

确认模型产生 Tool Call，而不是直接猜时间。

---

# Chapter 09：Long-term Memory

## 真实检查点

```text
15a8a8427db9801f1fcc01da5d15cfdb97014111  添加长期记忆
```

## 为什么不能无限塞聊天历史？

```text
聊天越来越多
  ↓
Prompt 越来越长
  ↓
Token 成本增加
  ↓
速度下降
  ↓
最终可能超过 Context Window
```

## 当前 AiFriends 方案

```text
最近 10 条 Message 原文
        +
Friend.memory 压缩摘要
        ↓
当前聊天上下文
```

## Memory 更新

```text
旧 Friend.memory
       +
最近 10 条聊天
       ↓
MemoryGraph
       ↓
LLM 总结
       ↓
新的 Friend.memory
```

当前每 5 条 Message 触发一次 `update_memory(friend)`。

## 教学化源码

```text
backend/web/views/friend/message/memory/graph.py
backend/web/views/friend/message/memory/update.py
backend/web/views/friend/message/chat/chat.py
```

## 动手实验

告诉 AI：

```text
我叫小明。
我喜欢蓝色。
我养了一只叫豆豆的猫。
```

经过多轮聊天后，在 Django Admin 中检查：

```text
Friend.memory
```

再问：

```text
我的猫叫什么？
```

## 验收

你能解释：

> “数据库存聊天记录”和“LLM 具有长期记忆”为什么不是同一件事？

---

# Chapter 10：RAG 与 LanceDB

## 真实检查点

```text
57f4c78c35313360065169c8ff008c77bba914a4  添加知识库
4c099063991521cdb55e58171919d2b623110d77  添加创建向量数据库的代码
```

## RAG 要分两阶段理解

### A. 建库

```text
data.txt
  ↓
TextLoader
  ↓
Document
  ↓
RecursiveCharacterTextSplitter
  ↓
Chunks
  ↓
CustomEmbeddings
  ↓
Vectors
  ↓
LanceDB
```

### B. 查询

```text
User Question
  ↓
Embedding
  ↓
Query Vector
  ↓
LanceDB similarity_search(k=3)
  ↓
Top 3 Documents
  ↓
Tool Result
  ↓
LLM
```

## 为什么要 Chunk？

用户问的是文档中的局部问题。

如果整份文档只有一个超大向量：

- 检索粒度很粗；
- 很难准确命中某一小段；
- 返回 LLM 的上下文也会过长。

当前参数：

```python
chunk_size=500
chunk_overlap=50
```

## 为什么要 Embedding？

Embedding 把：

```text
"如何使用某项功能？"
```

转换成：

```text
[0.12, -0.31, ..., 0.09]
```

向量数据库比较的是向量相似度，而不是简单字符串完全匹配。

## 教学化源码

```text
backend/web/documents/utils/custom_embeddings.py
backend/web/documents/utils/insert_documents.py
backend/web/views/friend/message/chat/graph.py
```

## 动手任务

1. 在 `data.txt` 写入只有你知道的一段资料；
2. 重新建 LanceDB；
3. 在聊天中提问；
4. 确认 Agent 调用了 `search_knowledge_base()`；
5. 确认最终答案基于检索文本。

## 验收

你能说清：

```text
Loader
Splitter
Embedding
VectorStore
Retrieval
LLM
```

每一层分别负责什么。

---

# Chapter 11：ASR —— 声音转文字

## 真实检查点

```text
02cbc4f7567ebbed95eba483724611c35b6f6b1f  实现前端语音输入
5c0f6473fefad53542280257399d830663c8683a  实现语音识别后端
```

## ASR

```text
Automatic Speech Recognition
声音 → 文字
```

## 当前链路

```text
Browser Microphone
  ↓
PCM
  ↓ HTTP
ASRView
  ↓
WebSocket
  ↓
ASR Service
  ↓
transcription text
  ↓
InputField.handleSend(text)
```

## 最重要的工程思想

键盘和语音不要实现两套聊天后端。

```text
Keyboard ─┐
          ├─> handleSend() -> 同一个 Chat API
ASR Text ─┘
```

## 验收

说一句话后，先能看到正确文字，再由同一个聊天链发送给 AI。

---

# Chapter 12：TTS —— AI 边生成边说话

## 真实检查点

```text
845dcb620d0ce2f77f50b8c8dc94b91de338a58b  实现语音合成后端
8615f6607406be373ae9ce7b09934d5a4da496c6  实现前端播放声音
88343a97f0d74570e10bfe3952c0192669876a61  实现音色的自由选择
```

## TTS

```text
Text To Speech
文字 → 声音
```

## 最简单但延迟高的设计

```text
LLM 生成完整文本
  ↓
TTS 生成完整 MP3
  ↓
前端播放
```

用户需要等两次完整过程。

## 当前 AiFriends 设计

```text
LLM chunk
  ├─> SSE content -> Browser text
  └─> TTS WebSocket
          ↓
       MP3 bytes
          ↓ Base64
       Queue
          ↓
       SSE audio
          ↓
       Browser MediaSource
```

## 为什么出现 Thread + asyncio + Queue？

当前代码同时连接：

```text
同步 Django StreamingHttpResponse
异步 LangGraph astream()
异步 TTS WebSocket
```

所以使用：

```text
Background Thread
  ↓
asyncio.run()
  ↓
LLM + TTS async tasks
  ↓
Queue
  ↓
同步 event_stream()
  ↓
SSE
```

## 前端为什么要 MediaSource？

因为收到的不是一个完整 mp3 文件 URL，而是：

```text
chunk1
chunk2
chunk3
...
```

前端处理：

```text
Base64
 ↓ atob
Uint8Array
 ↓
audioQueue
 ↓
SourceBuffer.appendBuffer()
 ↓
Audio
```

## 教学化源码

```text
backend/web/views/friend/message/chat/chat.py
frontend/src/components/character/chat_field/input_field/InputField.vue
```

## 验收

AI 还没有生成完全部文字时，浏览器已经开始播放前面的语音。

---

# Chapter 13：毕业练习 —— 追踪完整请求链

完成前面章节以后，用下面问题测试自己。

用户输入：

```text
请根据知识库回答 XXX
```

你必须能独立回答：

1. 哪个 Vue 组件接收输入？
2. `v-model` 绑定哪个变量？
3. `handleSend()` 做了什么？
4. `streamApi()` 请求哪个 API？
5. JWT 在哪里进入 Header？
6. Django 哪个 URL rule 匹配？
7. 哪个 APIView 接收请求？
8. 如何确认 `friend_id` 属于当前用户？
9. SystemPrompt 在哪里加入？
10. Character.profile 在哪里加入？
11. Friend.memory 在哪里加入？
12. 最近 10 条 Message 在哪里加入？
13. `CharGraph.create_app()` 创建了什么？
14. `bind_tools()` 做了什么？
15. `ToolNode` 做了什么？
16. 为什么进入 `search_knowledge_base()`？
17. 查询文本在哪里 Embedding？
18. LanceDB 的 `similarity_search(k=3)` 返回什么？
19. Tool result 怎样重新回到 Agent？
20. LLM 的文本 chunk 怎样进入 Queue？
21. 同一文本 chunk 怎样进入 TTS？
22. TTS 的 bytes 为什么要 Base64？
23. `event_stream()` 怎样 yield SSE？
24. 前端怎样区分 `content` 和 `audio`？
25. AI 气泡怎样不断追加文字？
26. Base64 怎样恢复为 Uint8Array？
27. SourceBuffer 怎样连续播放？
28. 完整回复怎样写入 Message？
29. token usage 保存在哪里？
30. 什么条件触发 `update_memory(friend)`？

如果这些问题能不看答案全部讲清楚，你已经从“复制项目”进入了“理解系统”。

---

# 4. 每章统一使用这套学习方法

## Step 1：先说需求

不要说：

> 我要学习 SSE。

先说：

> 模型要等 10 秒才显示答案，我希望它边生成边显示。

技术应该从需求出现。

---

## Step 2：先做最简单版本

例如聊天：

```text
POST -> LLM -> JSON
```

---

## Step 3：观察问题

```text
等待时间太长
```

---

## Step 4：引入新技术

```text
SSE
```

---

## Step 5：观察新复杂度

例如：

```text
SSE 连接里的 JWT 过期怎么办？
```

---

## Step 6：抽象公共能力

于是出现：

```text
streamApi.js
```

这就是工程学习。

---

# 5. 如何阅读真实 Commit

先：

```bash
git show --stat <sha>
```

回答：

> 改了哪些文件？

再：

```bash
git show <sha>
```

阅读 diff 时持续问：

1. 这个 commit 解决什么用户问题？
2. 为什么需要修改这些文件？
3. 数据从哪里进入？
4. 最终结果到哪里？
5. 如果删掉新增代码，什么功能会坏？

---

# 6. 推荐自己的 Commit 粒度

不要一整章只 commit 一次。

例如 SSE 章节可以写成：

```bash
git commit -m "learn: create basic chat api"
git commit -m "learn: convert chat response to streaming"
git commit -m "learn: emit sse chunks"
git commit -m "learn: receive sse in vue"
git commit -m "learn: append streamed ai text"
```

这样以后能清楚看到思考过程。

---

# 7. 最常见的错误学习方式

## 错误 1：复制最终代码，运行成功就算学会

运行成功只说明代码能工作。

真正学会的标准是：

> 删除代码以后，你能根据需求重新写出来。

---

## 错误 2：先把 LangChain 所有 API 学完

LangChain 很大。

AiFriends 当前真正核心的部分是：

```text
Messages
ChatOpenAI
Tool
Embeddings
VectorStore
```

先围绕项目需求学这些。

---

## 错误 3：一上来学多 Agent

先写懂：

```text
START -> agent -> END
```

再写懂：

```text
agent -> tools -> agent
```

然后再学习复杂图。

---

## 错误 4：认为 RAG = 向量数据库

完整 RAG 是：

```text
Load
 ↓
Chunk
 ↓
Embedding
 ↓
Store
 ↓
Query Embedding
 ↓
Retrieve
 ↓
Context
 ↓
Generate
```

LanceDB 只是中间的存储/检索层。

---

# 8. 毕业后必须做自己的改造

不要最后得到一个“和原项目完全一样”的复制品就停止。

至少增加 3 项自己的功能。

## 方向 A：多模型

例如：

```text
DeepSeek
GPT-compatible provider
其他 OpenAI-compatible provider
```

## 方向 B：更细的记忆系统

从一个 `Friend.memory` 继续拆成：

```text
用户长期画像
偏好记忆
人物关系
重要事件
短期工作记忆
```

## 方向 C：用户可上传知识库

从固定：

```text
data.txt
```

升级成：

```text
PDF / TXT 上传
 ↓
解析
 ↓
切块
 ↓
Embedding
 ↓
LanceDB
```

## 方向 D：更多 Tools

例如：

```text
天气
搜索
日历
数据库查询
```

## 方向 E：工程化

例如：

```text
Docker
PostgreSQL
Redis
Celery
测试
CI/CD
```

---

# 9. 毕业检查表

## 前端

- [ ] 理解 Vue `ref`
- [ ] 理解 props / emits
- [ ] 会写 Router
- [ ] 会写 Pinia store
- [ ] 会调 REST API
- [ ] 会用 Network 调试
- [ ] 会处理 SSE
- [ ] 理解 MediaSource

## Django

- [ ] 理解 URL → View → Model
- [ ] 会 Migration
- [ ] 会 Admin
- [ ] 会 APIView
- [ ] 理解 JWT 权限
- [ ] 会 ORM ForeignKey 查询
- [ ] 会 StreamingHttpResponse

## LangChain

- [ ] 理解 System/Human/AI Message
- [ ] 会调用 OpenAI-compatible LLM
- [ ] 理解 token usage
- [ ] 理解 Embedding
- [ ] 理解 VectorStore

## LangGraph

- [ ] 会定义 State
- [ ] 会定义 Node
- [ ] 会连 Edge
- [ ] 会写 Conditional Edge
- [ ] 理解 `@tool`
- [ ] 理解 `bind_tools()`
- [ ] 理解 `ToolNode`

## AI 应用

- [ ] 理解短期上下文
- [ ] 理解长期记忆压缩
- [ ] 理解 RAG
- [ ] 理解 ASR
- [ ] 理解 TTS
- [ ] 能完整追踪一条聊天数据流

---

# 10. 下一步阅读

- [零基础完整运行与复刻教程](./BEGINNER_TUTORIAL.md)
- [学习中心](./README.md)
- [系统架构与请求链路](./ARCHITECTURE.md)
- [常见报错排查](./TROUBLESHOOTING.md)
- [项目首页](../README.md)

推荐顺序：

```text
项目 README
  ↓
docs/README.md
  ↓
COURSE_REBUILD.md
  ↓
BEGINNER_TUTORIAL.md（具体命令和操作）
  ↓
带中文教学注释的核心源码
  ↓
ARCHITECTURE.md（系统复盘）
```
