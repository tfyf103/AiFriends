# AiFriends 从 0 复刻课程：按真实 Git 历史学习全栈 + LangChain

> 这不是一份“把最终代码从头到尾念一遍”的教程。
>
> 这套课程直接利用 AiFriends 自己的真实 Git 提交历史，把项目重新拆回它最初成长的样子：先有 Vue 页面，再有 Django 数据库和登录，再有角色系统、好友系统、聊天、流式输出、LangGraph、长期记忆、RAG，最后接入语音。
>
> 学习目标不是“看懂仓库”，而是：**你能在一个空目录里，按章节一步一步重新做出一个自己的 AiFriends。**

---

## 1. 为什么推荐“按版本复刻”，而不是直接读最终代码？

最终版 AiFriends 同时包含：

- Vue 3
- Vue Router
- Pinia
- Axios
- JWT
- Django
- Django REST Framework
- SQLite
- SSE
- LangChain
- LangGraph
- Function Calling
- 长期记忆
- Embedding
- LanceDB
- RAG
- ASR
- TTS
- WebSocket
- MediaSource

如果你第一天就打开最终版 `chat.py`，会同时看到线程、异步、WebSocket、SSE、LLM、TTS 和数据库。

这对零基础非常不友好。

但项目真实的开发历史不是“一天写完这些东西”，而是逐层增加能力：

```text
静态 Vue 页面
    ↓
路由
    ↓
注册登录
    ↓
Django 数据库
    ↓
角色 CRUD
    ↓
好友系统
    ↓
普通聊天
    ↓
SSE 流式聊天
    ↓
系统提示词 / 多轮上下文
    ↓
Tool Calling
    ↓
长期记忆
    ↓
RAG
    ↓
语音输入
    ↓
语音输出
```

所以最自然的学习顺序，就是沿着真实提交历史重新走一遍。

---

# 2. 两种学习模式

## 模式 A：只观察历史版本

适合想先理解作者“每一步改了什么”的同学。

查看某次提交：

```bash
git show <commit-sha>
```

例如：

```bash
git show b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

你会看到“实现文字交流的后端流式输出”到底改了哪些文件、增加了哪些代码。

比较两个阶段：

```bash
git diff <旧版本> <新版本>
```

例如比较普通聊天和第一次流式聊天：

```bash
git diff 72a9866e3370481a8fa6e070e55c7784977c058a b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

---

## 模式 B：真的切到旧版本运行

你可以临时进入某个历史版本：

```bash
git switch --detach <commit-sha>
```

例如：

```bash
git switch --detach 72a9866e3370481a8fa6e070e55c7784977c058a
```

这时 Git 会提示你处于 `detached HEAD`，这是正常现象。

### 重要：不要直接在 detached HEAD 上长期开发

如果你想从某个历史阶段开始自己写：

```bash
git switch -c learn/chapter-05 72a9866e3370481a8fa6e070e55c7784977c058a
```

学习结束想回到教程分支：

```bash
git switch agent/beginner-tutorial
```

或者回主分支：

```bash
git switch main
```

---

# 3. 最推荐的复刻方式：另建一个学习仓库

真正想学会，最好不要只在原仓库切版本。

建议新建：

```text
AiFriends-Learning/
```

然后每完成一章自己提交一次：

```bash
git add .
git commit -m "learn: chapter 01 vue shell"
```

你自己的 commit 不需要和原项目一模一样。

原项目 commit 是“参考答案”；你的 commit 是“学习轨迹”。

---

# 4. 课程总览

| 章 | 主题 | 核心技术 | 学完必须能回答 |
|---|---|---|---|
| 00 | 环境与项目骨架 | Git / Python / Node | 前端和后端为什么要分别启动？ |
| 01 | Vue 页面与路由 | Vue / Router | URL 怎么决定显示哪个页面？ |
| 02 | Django 与数据库 | Django / ORM / SQLite | Model 为什么能变成数据库表？ |
| 03 | 注册登录 | REST / JWT / Pinia / Axios | 登录状态如何贯穿前后端？ |
| 04 | AI 角色 CRUD | FormData / ImageField / CRUD | 一个角色怎样从表单进入数据库？ |
| 05 | 首页与好友系统 | API / 关系模型 | 用户、角色、好友是什么关系？ |
| 06 | 普通聊天 | LangChain / LLM | 一条消息怎样进入模型？ |
| 07 | SSE 流式聊天 | StreamingHttpResponse / SSE | 为什么文字能一个片段一个片段出现？ |
| 08 | 多轮上下文与 Tool | Message / LangGraph | Agent 为什么能自己决定调用工具？ |
| 09 | 长期记忆 | Prompt / Summarization | 为什么不能无限塞历史聊天？ |
| 10 | RAG | Embedding / LanceDB | 向量数据库到底解决什么问题？ |
| 11 | ASR | PCM / WebSocket | 声音怎么变成文字？ |
| 12 | TTS | asyncio / Queue / MediaSource | AI 回复为什么能边生成边说话？ |
| 13 | 最终整合 | Full Stack | 能否独立追踪完整请求链路？ |

---

# Chapter 00：先搭一个“什么都不会”的开发环境

## 学习目标

这一章完全不碰 LangChain。

你只需要理解：

```text
Git = 管代码版本
Python = 跑 Django 后端
Node.js = 跑 Vue/Vite 前端工具链
浏览器 = 运行最终前端 JavaScript
```

## 原项目起点

首次提交：

```text
cd5cfb2b387f4fb727cd55f33db36ac3a2a847f7
首次提交：上传本地项目
```

## 动手任务

安装：

- Git
- Python
- Node.js
- VS Code

确认：

```bash
git --version
python --version
node --version
npm --version
```

创建：

```text
aifriends-learning/
├── backend/
└── frontend/
```

## 本章不要做

不要安装 LangChain。
不要创建向量数据库。
不要研究 Agent。

先建立“前端和后端是两个程序”的概念。

## 验收标准

你能解释：

> 为什么 `npm run dev` 和 `python manage.py runserver` 要在两个终端运行？

---

# Chapter 01：先让 Vue 页面跑起来

## 真实历史检查点

```text
e03219b7464ea487f843f7abe74daa98eb7dfd7c  创建导航栏
b1703e8eff39f95dcd8cf3ed7b5d1def0e616758  实现路由
b938159da24699eaec1249251b99ec06884f6b0a  实现登录注册页面
```

## 要学的知识

### Vue 最小心智模型

```text
main.js
  ↓
createApp(App)
  ↓
App.vue
  ↓
组件树
```

### Router 心智模型

```text
浏览器 URL
  ↓
Vue Router
  ↓
匹配 routes
  ↓
显示某个 View
```

## 动手任务

自己做 3 个页面：

```text
/
/login
/register
```

先不要请求 Django。

页面上只需要有：

- 导航栏
- 登录表单
- 注册表单

## 必须理解

```vue
<script setup>
</script>

<template>
</template>

<style scoped>
</style>
```

以及：

```js
ref()
computed()
defineProps()
defineEmits()
```

## 验收

手动输入：

```text
http://localhost:5173/login
```

应该看到登录页面，并且页面切换不刷新整个浏览器。

---

# Chapter 02：Django、Model 和 SQLite

## 真实历史检查点

```text
3ab2bd28ca6551e188084e7502de82a06df96b0a  实现完数据库
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  实现后端
```

## 先理解 Django 的 4 个角色

```text
URL
 ↓
View
 ↓
Model
 ↓
Database
```

### URL

回答：

> 用户访问哪个地址？

### View

回答：

> 收到请求以后做什么？

### Model

回答：

> 数据长什么样？

### Database

回答：

> 数据最终保存在哪里？

## 动手任务

自己创建 Django 项目和 app：

```bash
django-admin startproject backend
python manage.py startapp web
```

创建最简单的用户扩展资料 Model。

然后执行：

```bash
python manage.py makemigrations
python manage.py migrate
```

## 必须学会看 migration

不要把：

```bash
python manage.py migrate
```

理解成“神奇数据库命令”。

要知道流程：

```text
models.py
   ↓ makemigrations
migration 文件
   ↓ migrate
SQLite 表结构
```

## 验收

能打开：

```text
http://127.0.0.1:8000/admin/
```

并理解为什么需要：

```bash
python manage.py createsuperuser
```

---

# Chapter 03：把 Vue 登录页真正接到 Django

## 真实历史检查点

```text
a27cbf8f90cf256ab075173f19d468319b302f67  前端对接注册、登录、退出api
b0aa1d5c169d836023fd3788152d5cb1eb4bf55b  刷新页面时动态拉取用户信息
e2915586d6352180b93500ce8e15dbfa8afa8704  创建更新用户资料后端api
8d06c1ec8c04a70a8a47a1644fd8cd28a63a48e6  实现编辑资料页面前端
```

## 本章最重要的一张图

```text
登录表单
  ↓ axios POST
Django LoginView
  ↓ 校验用户名密码
access token + refresh token
  ↓
Pinia 保存 access token
  ↓
以后请求：Authorization: Bearer xxx
```

## 学 JWT 时不要死背术语

先回答：

### 为什么不能每个请求都重新输入密码？

所以需要 token。

### 为什么 access token 不设置成永不过期？

因为泄露风险太高。

### access token 过期了怎么办？

用寿命更长的 refresh token 换一个新的 access token。

## 动手任务

完成：

```text
POST /api/user/account/register/
POST /api/user/account/login/
POST /api/user/account/logout/
POST /api/user/account/refresh_token/
GET  /api/user/account/get_user_info/
```

前端完成：

```text
Pinia user store
Axios request interceptor
Axios response interceptor
Router login guard
```

## 调试要求

打开 DevTools -> Network。

你必须亲眼看到：

```text
Authorization: Bearer eyJ...
```

而不是只满足于“页面登录成功了”。

---

# Chapter 04：角色 CRUD —— 第一次完整前后端业务

## 真实历史检查点

```text
2081304f049a58a404b39bfe09f9c373b80d24df  实现角色增删改查后端api
1c811b7034f042ed5344efe653e0a31e07c6e00a  给增删改查后端api打补丁
84f1c92eba32c62ef2e5724a77eeb7c64979de6b  实现完创建虚拟角色前端
95cf0456ef46696bca36c602928fbbb6dbe658d5  实现更新虚拟角色前端页面
```

## CRUD 是什么？

```text
Create  创建
Read    查询
Update  修改
Delete  删除
```

几乎所有 Web 系统都离不开 CRUD。

## 本章重点 Model

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

普通 JSON 可以传：

```json
{"name":"Alice"}
```

图片不能简单当普通 JSON 字符串处理。

所以你需要理解：

```text
FormData
multipart/form-data
Django ImageField
MEDIA_ROOT
MEDIA_URL
```

## 动手任务

做出：

- 创建角色
- 查看角色
- 修改角色
- 删除角色
- 上传头像
- 上传背景图

## 验收

不要只看数据库。

必须做到：

```text
Vue 表单
  ↓
HTTP
  ↓
Django View
  ↓
Character Model
  ↓
SQLite + media 文件
  ↓
再次 GET
  ↓
Vue 正确显示
```

---

# Chapter 05：首页、搜索与好友系统

## 真实历史检查点

```text
f96da725bbfd77aa9766f70786a6061f35f8dcb9  实现首页前后端
c9ea5e0f3b1a276c3fe6d0b10fa648db3f5510ca  实现搜索功能
102b31a0f60be51bbc01da5d15cfdb97014111     （不要使用，本行仅作为格式说明）
102b31a0f60be51bbc6f22f690ec74d3ee0a5be3  实现好友页面后端
fb1394362c3ba60bee544bf8737bca5051ea9ae8  实现聊天框
1c9d9e000c77c4e1779e0681ae5fca7e8123dc67  实现好友列表前端
```

> 注意：学习时以完整 40 位 SHA 为准；上面标注“不要使用”的示例行故意展示了为什么复制 SHA 时不能手打。

## 本章要理解关系数据库

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

Friend 不是“另一个用户”。

它表达的是：

> 某个用户和某个 AI Character 建立了一条好友/聊天关系。

## 动手任务

完成：

- 首页角色列表
- 搜索角色
- 添加好友
- 好友列表
- 删除好友
- 打开聊天弹窗

## 验收

你能解释下面查询的含义：

```python
Friend.objects.filter(me__user=request.user)
```

如果看不懂 Django ORM 的双下划线关联查询，先不要进入聊天章节。

---

# Chapter 06：先做“不会流式输出”的普通 AI 聊天

## 真实历史检查点

```text
c82553f13badf75ba372f1bc343b0d14b0bc5081  创建消息数据库
72a9866e3370481a8fa6e070e55c7784977c058a  实现聊天后端
```

## 本章原则

这一章故意不要做 SSE。
不要做 TTS。
不要做 RAG。

先做最普通的：

```text
用户输入
  ↓ POST
Django
  ↓
LLM
  ↓
完整答案
  ↓ JSON
浏览器
```

## LangChain 先只学 3 个东西

```python
HumanMessage
SystemMessage
ChatOpenAI
```

先理解：

```python
llm.invoke(messages)
```

再往后学 Agent。

## Message Model

必须理解为什么聊天记录需要：

```text
friend
user_message
output
input_tokens
output_tokens
total_tokens
create_time
```

## 验收

输入：

```text
你好
```

浏览器等待模型生成完，然后一次性看到完整回复。

只有这一章跑通，才进入 SSE。

---

# Chapter 07：把普通聊天升级为 ChatGPT 式 SSE 流式输出

## 真实历史检查点

```text
b9ea1c3404b04413d638067de78c3ed4d7262fc3  实现文字交流的后端流式输出
3c7c464b51dcbb411ad50bafe58ad214ecc6eb2c  改造成流式前端回复
031f03137cf8abb5128c3de93bc6f353b93965cf  实现聊天记录的后端
ea419695f4d8e9e2cec97c4f92a03dc7d679e4df  实现聊天记录的流式加载（前后端）
7ba85a3b629a9fdb41307fb6427960ffe674c2b9  流式加载每次返回10条消息
```

## 为什么普通 axios 不够？

普通模式：

```text
请求 ───────────── 等 ─────────────> 完整响应
```

流式模式：

```text
请求
  <─ token 1
  <─ token 2
  <─ token 3
  <─ token 4
  <─ [DONE]
```

## SSE 最小格式

```text
data: {"content":"你"}


data: {"content":"好"}


data: [DONE]

```

## 必须理解

后端：

```python
StreamingHttpResponse

yield "data: ...\n\n"
```

前端：

```text
fetchEventSource
onopen
onmessage
onerror
```

当前教学分支中的重点源码：

```text
frontend/src/js/http/streamApi.js
frontend/src/components/character/chat_field/input_field/InputField.vue
backend/web/views/friend/message/chat/chat.py
```

这些文件已经加入逐段中文教学注释。

## 验收

DevTools -> Network 中保持一个长连接，页面文字逐渐增长，而不是最后突然出现完整答案。

---

# Chapter 08：系统提示词、多轮对话、Function Calling 与 LangGraph

## 真实历史检查点

```text
3bcc4a8c8e169475af6c78b2ac19752b62625bdf  添加系统提示词和多轮记忆对话
72c4c3ae5efb950e7b4f08cded3a37238e961c78  实现function call
```

## 从“聊天模型”升级成“Agent”

普通模型：

```text
messages -> LLM -> answer
```

Agent：

```text
messages
   ↓
LLM
   ↓
要不要调用工具？
   ├─ 不需要 -> answer
   └─ 需要
       ↓
      Tool
       ↓
    Tool result
       ↓
      LLM
       ↓
     answer
```

## 本章 LangGraph 关键词

```text
StateGraph
AgentState
add_messages
add_node
add_edge
add_conditional_edges
ToolNode
START
END
```

## 当前真实代码

```text
backend/web/views/friend/message/chat/graph.py
```

重点理解：

```python
llm.bind_tools(tools)
```

不是“执行工具”。

它只是把工具描述告诉模型。

真正执行：

```python
ToolNode(tools)
```

## 第一个练习 Tool

自己写：

```python
@tool
def get_time() -> str:
    ...
```

不要一上来写复杂搜索 Agent。

## 验收

问：

```text
现在几点？
```

确认模型真正产生 tool call，而不是凭语言模型记忆瞎猜时间。

---

# Chapter 09：长期记忆

## 真实历史检查点

```text
15a8a8427db9801f1fcc01da5d15cfdb97014111  添加长期记忆
```

## 为什么需要长期记忆？

假设 1000 轮聊天全部放进 prompt：

```text
成本越来越高
上下文越来越长
响应越来越慢
可能超过模型 context window
```

所以当前项目采用：

```text
最近 10 条原文
       +
Friend.memory 摘要
       ↓
本轮模型上下文
```

## 记忆更新

```text
旧 Friend.memory
       +
最近 10 条聊天
       ↓
MemoryGraph
       ↓
新的 Friend.memory
```

当前代码每 5 条 Message 触发一次更新。

重点文件：

```text
backend/web/views/friend/message/memory/graph.py
backend/web/views/friend/message/memory/update.py
backend/web/views/friend/message/chat/chat.py
```

## 动手实验

连续告诉 AI：

```text
我叫小明。
我最喜欢蓝色。
我养了一只叫豆豆的猫。
```

继续聊若干轮后检查 Django Admin 中的 `Friend.memory`。

然后开启一个后续对话：

```text
我最喜欢什么颜色？
```

## 必须理解

长期记忆不是数据库“自动记住”。

它本质上仍是一次 LLM 信息压缩任务。

---

# Chapter 10：RAG —— 给 Agent 一本它可以查的资料

## 真实历史检查点

```text
57f4c78c35313360065169c8ff008c77bba914a4  添加知识库
4c099063991521cdb55e58171919d2b623110d77  添加创建向量数据库的代码
```

## RAG 分两阶段

### 建库

```text
data.txt
  ↓ TextLoader
Document
  ↓ RecursiveCharacterTextSplitter
Chunks
  ↓ Embedding
Vectors
  ↓ LanceDB
```

### 检索

```text
用户问题
  ↓ Embedding
Query Vector
  ↓ LanceDB similarity_search
Top-K 文本
  ↓ Tool result
LLM
```

重点文件：

```text
backend/web/documents/utils/custom_embeddings.py
backend/web/documents/utils/insert_documents.py
backend/web/views/friend/message/chat/graph.py
```

## 先学 Chunk，不要先背“向量数据库”定义

思考：

> 一本 300 页 PDF，用户只问其中一句，为什么不能把整本 PDF 每次都交给 LLM？

因此需要先切小块。

当前参数：

```python
chunk_size=500
chunk_overlap=50
```

## Embedding 实验

你不需要手算 1024 个浮点数。

只需要建立概念：

```text
"Python 是编程语言"
          ↓
[0.123, -0.42, ...]
```

相似语义 -> 向量空间距离通常更近。

## 验收

向 `data.txt` 写入一段只有知识库知道的资料。

重新建库。

然后在聊天中提问，确认：

```text
agent
  ↓ tool_call
search_knowledge_base
  ↓
LanceDB Top 3
  ↓
agent
  ↓
最终回答
```

---

# Chapter 11：ASR —— 让浏览器说话而不是打字

## 真实历史检查点

```text
02cbc4f7567ebbed95eba483724611c35b6f6b1f  实现前端语音输入
5c0f6473fefad53542280257399d830663c8683a  实现语音识别后端
```

## ASR 是什么？

```text
Automatic Speech Recognition
自动语音识别
```

功能方向：

```text
声音 -> 文字
```

不是：

```text
文字 -> 声音
```

后者叫 TTS。

## 当前链路

```text
Microphone
  ↓
PCM
  ↓ HTTP 上传
ASRView
  ↓ WebSocket
ASR Service
  ↓
transcription
  ↓
文字
  ↓
handleSend(text)
```

关键设计：

语音识别完成后，不再创建第二套聊天逻辑。

它最终仍调用同一个：

```text
InputField.handleSend()
```

所以：

```text
键盘输入 ─┐
          ├─> handleSend -> 同一个聊天接口
语音输入 ─┘
```

这叫“复用业务链路”。

---

# Chapter 12：TTS —— AI 一边生成文字，一边开始说话

## 真实历史检查点

```text
845dcb620d0ce2f77f50b8c8dc94b91de338a58b  实现语音合成后端
8615f6607406be373ae9ce7b09934d5a4da496c6  实现前端播放声音
88343a97f0d74570e10bfe3952c0192669876a61  实现音色的自由选择
```

## TTS 是什么？

```text
Text To Speech
文字 -> 声音
```

## 最简单实现

可以先做：

```text
LLM 完整回答
  ↓
完整文本发送 TTS
  ↓
等待完整 MP3
  ↓
播放
```

但是用户会等很久。

AiFriends 当前更进一步：

```text
LLM token/chunk 1 ──> 前端显示
        └──────────> TTS
                      ↓
                   MP3 chunk ──> 前端播放

LLM token/chunk 2 ──> 前端显示
        └──────────> TTS
                      ↓
                   MP3 chunk ──> 前端播放
```

## 为什么后端出现 asyncio + threading + Queue？

因为这里同时存在：

```text
同步 Django StreamingHttpResponse
异步 LangGraph astream
异步 WebSocket TTS
```

当前实现用：

```text
后台 Thread
  ↓
asyncio.run(...)
  ↓
LLM + TTS async tasks
  ↓
Queue
  ↓
同步 event_stream()
  ↓
SSE
```

## 为什么浏览器用 MediaSource？

因为收到的不是一个完整 MP3 URL。

而是：

```text
chunk 1
chunk 2
chunk 3
...
```

所以前端需要：

```text
Base64
  ↓ atob
Uint8Array
  ↓
audioQueue
  ↓
SourceBuffer.appendBuffer
  ↓
Audio 播放
```

重点文件：

```text
backend/web/views/friend/message/chat/chat.py
frontend/src/components/character/chat_field/input_field/InputField.vue
```

---

# Chapter 13：最终整合 —— 从一条消息追踪整个系统

完成前 12 章以后，不要急着增加新功能。

先完成下面这个终极练习。

## 任务

用户输入：

```text
请告诉我知识库中关于 XXX 的信息
```

你必须能在纸上或 Markdown 中完整写出：

```text
1. 哪个 Vue input 接收到文字？
2. 哪个 ref 保存它？
3. handleSend 做了什么？
4. streamApi 发向哪个 URL？
5. JWT 在哪加进 Header？
6. Django 哪个 urlpatterns 匹配？
7. 哪个 View 接收请求？
8. 怎样校验 friend 属于当前 user？
9. SystemPrompt 在哪里加入？
10. Character.profile 在哪里加入？
11. Friend.memory 在哪里加入？
12. 最近聊天记录在哪里加入？
13. CharGraph 怎么创建？
14. LLM 怎么知道有哪些 tools？
15. 为什么进入 ToolNode？
16. search_knowledge_base 怎样连接 LanceDB？
17. query 怎样变成 embedding？
18. similarity_search(k=3) 返回什么？
19. Tool result 怎样回到 agent？
20. LLM 文本怎样变成 BaseMessageChunk？
21. 文本怎样进入 Queue？
22. 文本怎样进入 TTS WebSocket？
23. MP3 bytes 怎样变成 Base64？
24. event_stream 怎样 yield SSE？
25. 前端 onmessage 怎样区分 content/audio？
26. 文本怎样追加到 AI 气泡？
27. Base64 怎样变回 Uint8Array？
28. SourceBuffer 怎样连续播放？
29. 最终 Message 怎样写进 SQLite？
30. 什么时候触发 update_memory？
```

如果这 30 个问题你能独立回答，你已经不再是在“照着教程复制代码”。

你已经真正理解了 AiFriends。

---

# 5. 每章统一的学习模板

以后你自己学任何项目，也推荐按下面方式。

## Step 1：先说需求

例如：

> 我希望模型回复能边生成边显示。

而不是：

> 今天我要学 SSE API。

技术应该从需求长出来。

---

## Step 2：写最简单版本

例如先普通聊天：

```text
POST -> LLM -> JSON
```

---

## Step 3：发现问题

```text
模型 10 秒后才返回，体验不好。
```

---

## Step 4：引入新技术

```text
SSE
```

---

## Step 5：观察新复杂度

```text
SSE 不能直接走普通 axios 拦截器怎么办？
JWT 过期怎么重连？
```

---

## Step 6：继续抽象

于是产生：

```text
streamApi.js
```

这就是工程学习，而不是 API 背诵。

---

# 6. 如何阅读一个真实 commit

不要只看 commit 标题。

执行：

```bash
git show --stat <sha>
```

先看改了哪些文件。

然后：

```bash
git show <sha>
```

阅读 diff 时：

```text
+ 绿色：新增
- 红色：删除
```

问自己 4 个问题：

1. 这个 commit 想解决什么用户问题？
2. 为什么要修改这些文件？
3. 数据从哪里进，最后到哪里？
4. 如果删掉这一段，什么功能会坏？

---

# 7. 推荐自己的 commit 记录方式

不要一章写完所有内容后只 commit 一次。

例如 SSE 章节：

```bash
git commit -m "learn: return a basic Django response"
git commit -m "learn: convert response to StreamingHttpResponse"
git commit -m "learn: emit SSE data chunks"
git commit -m "learn: receive SSE in Vue"
git commit -m "learn: append streamed AI message"
```

半年以后重新看，你会非常清楚自己是怎样学会的。

---

# 8. 不建议的学习方法

## 误区 1：复制最终代码，运行成功就算学会

运行成功只说明：

> 代码能运行。

不代表：

> 你能自己重新写出来。

---

## 误区 2：先学完整 LangChain 文档再做项目

LangChain 很大。

AiFriends 实际只用了其中一部分核心概念。

先围绕当前需求学：

```text
Messages
ChatOpenAI
Tool
Embedding
VectorStore
```

再扩展。

---

## 误区 3：LangGraph 一上来就学复杂多 Agent

先把本项目的：

```text
START -> agent -> END
```

看懂。

然后再看：

```text
agent -> tools -> agent
```

这两个都能自己写以后，再学多 Agent。

---

## 误区 4：RAG = 向量数据库

不完整。

RAG 是一整条链：

```text
加载
切块
Embedding
存储
查询 Embedding
检索
把资料交给 LLM
生成回答
```

LanceDB 只是其中“存储 + 检索”的一层。

---

# 9. 完整毕业作品要求

不要仅复制 AiFriends。

最终给自己增加至少 3 个改造：

例如：

### 方向 A：多模型

```text
DeepSeek
GPT
Claude-compatible provider
```

### 方向 B：更好的记忆

区分：

```text
用户画像记忆
事件记忆
偏好记忆
短期工作记忆
```

### 方向 C：可上传知识库

从固定：

```text
data.txt
```

升级成：

```text
用户上传 PDF / TXT
  ↓
自动解析
  ↓
自动建库
```

### 方向 D：Agent Tools

新增：

```text
天气
搜索
日历
数据库查询
```

### 方向 E：工程化

新增：

```text
Docker
PostgreSQL
Redis
Celery
测试
CI/CD
```

---

# 10. 最终检查表

## 前端

- [ ] 能独立解释 Vue `ref`
- [ ] 能独立解释 props / emits
- [ ] 能写 Vue Router
- [ ] 能写 Pinia store
- [ ] 能用 Axios 调 API
- [ ] 能打开 DevTools Network 调试
- [ ] 能处理 SSE
- [ ] 能解释 MediaSource

## Django

- [ ] 理解 URL -> View -> Model
- [ ] 会 migrations
- [ ] 会 Django Admin
- [ ] 会 DRF APIView
- [ ] 会权限认证
- [ ] 会 ORM 外键查询
- [ ] 会 StreamingHttpResponse

## AI / LangChain

- [ ] 理解 SystemMessage / HumanMessage / AIMessage
- [ ] 会调用 ChatOpenAI-compatible API
- [ ] 理解 token usage
- [ ] 理解 Embedding
- [ ] 理解 VectorStore

## LangGraph

- [ ] 能自己写 StateGraph
- [ ] 理解 State
- [ ] 理解 Node
- [ ] 理解 Edge
- [ ] 理解 Conditional Edge
- [ ] 会写 Tool
- [ ] 理解 bind_tools
- [ ] 理解 ToolNode

## AI 应用能力

- [ ] 理解短期上下文
- [ ] 理解长期记忆压缩
- [ ] 理解 RAG
- [ ] 理解 ASR
- [ ] 理解 TTS
- [ ] 能追踪完整数据流

---

# 11. 继续阅读

- [零基础完整教程](./BEGINNER_TUTORIAL.md)
- [系统架构](./ARCHITECTURE.md)
- [常见报错排查](./TROUBLESHOOTING.md)
- [学习地图](./README.md)
- [项目首页](../README.md)

如果你是第一次接触全栈开发，建议顺序：

```text
README
  ↓
docs/README.md
  ↓
本文件 COURSE_REBUILD.md
  ↓
BEGINNER_TUTORIAL.md 对照具体操作
  ↓
直接阅读带中文教学注释的核心源码
```
