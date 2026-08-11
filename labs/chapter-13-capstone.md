# Chapter 13 Lab：毕业实验——完整追踪并改造一条 AiFriends 消息

## 本章目标

这一章不再教新的框架 API。

你要证明自己已经能把整个系统当作一个整体理解：

```text
输入
 ↓
Vue
 ↓
JWT / HTTP / SSE
 ↓
Django
 ↓
ORM
 ↓
LangChain / LangGraph
 ↓
Tool / RAG
 ↓
LLM
 ↓
TTS
 ↓
SSE
 ↓
MediaSource
 ↓
Message persistence
 ↓
Long-term Memory
```

最终要求：**独立完成一个小改造，并解释它影响了哪几层。**

---

# Part A：白纸画全链路

不要看文档，先在纸上写出：

> “用户在 InputField 输入一句话并按 Enter”之后会经过哪些文件？

至少应包含：

```text
InputField.vue
streamApi.js
web/urls.py
MessageChatView.post()
add_system_prompt()
add_recent_messages()
CharGraph.create_app()
agent
ToolNode（如果需要）
LLM stream
tts_sender / tts_receiver
Queue
event_stream()
SSE
InputField onmessage
MediaSource
Message.objects.create()
update_memory()
```

### 验收

完成后再对照：

- [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
- 教学注释版 `chat.py`
- 教学注释版 `graph.py`

把漏掉的节点用另一种颜色补上。

---

# Part B：一次真实请求取证

打开：

```text
浏览器 DevTools → Network
Django 终端
```

发送一条：

```text
请告诉我当前精确时间。
```

记录：

```text
1. 请求 URL：
2. Method：
3. Authorization Header：
4. Request Body：
5. HTTP Content-Type：
6. 第一条 SSE data：
7. 是否触发 get_time Tool：
8. 最后一条 [DONE]：
9. 数据库 Message.id：
10. input_tokens/output_tokens：
```

### 验收

任何一个字段都必须通过真实运行证据获得，不允许凭印象填写。

---

# Part C：分别证明三种“记忆/知识”不是一回事

准备三个问题：

## 1. Character Profile

角色设定里写：

```text
你是一位住在月球基地的工程师。
```

问：

```text
你住在哪里？
```

## 2. Long-term Memory

聊天中告诉 AI：

```text
我最喜欢喝无糖冰美式。
```

触发长期记忆后问：

```text
我平时喜欢喝什么？
```

## 3. RAG

知识库 data.txt 放一条只有知识库知道的信息，再提问。

### 验收

你能解释三种数据分别从哪里进入：

```text
Character.profile
Friend.memory
LanceDB Tool result
```

并说明它们为什么不能简单合成同一个数据库字段。

---

# Part D：故障定位考试

下面每个故障只允许先检查一个层级。写出你第一步会看哪里。

### 故障 1

页面点击发送完全没有 Network 请求。

你的第一检查点：Vue event/handleSend，而不是 Django。

### 故障 2

Network 显示 401。

第一检查点：Authorization/access-refresh 流程。

### 故障 3

SSE 有 content，但页面没显示。

第一检查点：`streamApi onmessage → emit → history`。

### 故障 4

普通聊天正常，问知识库内容回答错误。

第一检查点：打印 similarity_search 返回的 docs。

### 故障 5

文字正常，音频没有。

第一检查点：确认 TTS WebSocket 是否收到 bytes，再向前端逐层查。

### 故障 6

AI 忘记很久以前的用户偏好。

第一检查点：Friend.memory 是否已经更新且是否被加入 SystemMessage。

---

# Part E：毕业改造（三选一）

请选择一个真正实现。

## 选题 A：新增 Character Greeting

给 Character 增加：

```text
greeting
```

目标：第一次打开聊天时显示角色自定义欢迎语。

你必须考虑：

```text
Model
Migration
Create API
Update API
Get API
Vue Create Form
Vue Update Form
Chat UI
```

### 加分

只在“没有任何 Message 的 Friend”中显示，已有聊天不重复插入。

---

## 选题 B：RAG 引用来源

知识库 Tool 返回：

```text
内容
source
chunk information
```

最终 AI 回复能附带简单来源。

你必须考虑：

```text
Document metadata
Tool return format
Prompt / Agent behavior
UI presentation（可选）
```

---

## 选题 C：聊天 Stop Generation

让用户能点击：

```text
停止生成
```

目标：

- 前端停止接受当前 SSE
- 停止音频播放
- 旧回调不再更新 UI
- 明确数据库应该保存“部分输出”还是“不保存”，并说明设计选择

你需要研究：

```text
AbortController / fetchEventSource cancellation
processId
MediaSource cleanup
server disconnect behavior
```

---

# Part F：毕业答辩问题

完成改造后，不看代码回答：

1. Vue 的响应式状态在聊天里有哪些？
2. 为什么普通 API 与 SSE 使用不同请求封装？
3. access token 和 refresh token 分别在哪里？
4. Django 如何确认 friend_id 属于当前用户？
5. `bind_tools()` 和 `ToolNode` 分别做什么？
6. 为什么 `tools → agent` 这条边不能少？
7. 短期聊天历史与 `Friend.memory` 有什么区别？
8. RAG 的“检索”发生在哪个函数？
9. Embedding 与生成模型是一回事吗？
10. ASR 与 TTS 的方向分别是什么？
11. 为什么音频在 SSE 里使用 Base64？
12. `Queue` 在当前 TTS 架构中解决什么桥接问题？
13. `Message` 表为什么保存 token usage？
14. 如果用户关闭 Chat Modal，哪些资源必须清理？
15. 你的毕业改造影响了哪些层？为什么？

如果能用自己的语言回答这些问题，你已经不只是“复刻了 AiFriends”，而是掌握了它背后的全栈 AI 工程模型。

---

# 最终验收 Checklist

- [ ] 我能从零启动前后端
- [ ] 我能使用 DevTools 定位请求问题
- [ ] 我能写一个新的 Django API
- [ ] 我能写一个新的 Vue 状态/组件交互
- [ ] 我能解释 JWT refresh
- [ ] 我能解释 SSE framing
- [ ] 我能解释 LangChain Message
- [ ] 我能画 LangGraph Agent 循环
- [ ] 我能自己写一个 Tool
- [ ] 我能独立检查 RAG retrieval 结果
- [ ] 我能解释 Friend.memory 更新流程
- [ ] 我能区分 ASR/TTS
- [ ] 我能解释 MediaSource audio queue
- [ ] 我完成了一个跨层改造
- [ ] 我为改造创建了自己的 Git commit

建议最后提交：

```bash
git add .
git commit -m "learn: complete AiFriends full-stack capstone"
```

然后用：

```bash
git log --oneline
```

回看你从 Chapter 00 到 Chapter 13 的成长轨迹。
