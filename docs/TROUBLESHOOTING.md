# AiFriends 常见报错与排查手册

> 新手最重要的能力不是“不报错”，而是能判断错误发生在哪一层。

---

# 1. 先学会定位层级

遇到问题先问：

```text
A. Python 环境？
B. Node 环境？
C. Django 启动？
D. Vue 启动？
E. 浏览器跨域？
F. JWT 登录？
G. 数据库？
H. LLM API？
I. LangGraph Tool？
J. LanceDB / Embedding？
K. ASR？
L. TTS / 浏览器音频？
```

不要看到“聊天失败”就直接改 LangChain。

---

# 2. `python` 命令不存在

现象：

```text
python: command not found
```

或 Windows：

```text
'python' is not recognized...
```

检查：

```bash
python --version
py --version
python3 --version
```

Windows 可能需要使用：

```bash
py
```

macOS / Linux 可能需要：

```bash
python3
```

后续命令相应替换即可。

---

# 3. Django 6 安装失败

先看 Python：

```bash
python --version
```

项目使用 Django 6.0.5，因此建议 Python 3.12+。

如果你是 Python 3.10 / 3.11，先升级 Python，不要强行修改依赖版本。

---

# 4. `ModuleNotFoundError: No module named 'dotenv'`

原因：

```python
backend/backend/settings.py
```

使用：

```python
from dotenv import load_dotenv
```

解决：

```bash
pip install -r requirements.txt
```

本教学分支已把：

```text
python-dotenv==1.2.2
```

加入 requirements。

验证：

```bash
python -c "from dotenv import load_dotenv; print('ok')"
```

---

# 5. 明明安装了依赖，Django 还是说找不到

最常见原因：你没有激活虚拟环境。

看终端前面有没有：

```text
(.venv)
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

再检查：

```bash
which python
```

Windows：

```cmd
where python
```

路径应该指向 `.venv`。

---

# 6. PowerShell 不允许激活脚本

可能出现 ExecutionPolicy 错误。

你可以临时为当前 PowerShell 会话设置：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

再执行：

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 7. `npm` / `node` 不存在

检查：

```bash
node -v
npm -v
```

重新安装 Node.js。

当前前端 `package.json` 要求：

```text
^20.19.0 或 >=22.12.0
```

---

# 8. `npm install` 报 Node engine 不匹配

先：

```bash
node -v
```

如果版本过旧，升级 Node。

不要优先使用：

```bash
--force
```

因为强制装上并不代表 Vite 能正常运行。

---

# 9. `python manage.py migrate` 找不到 `manage.py`

你很可能在错误目录。

正确：

```bash
cd AiFriends/backend
python manage.py migrate
```

确认当前目录：

macOS/Linux：

```bash
pwd
ls
```

Windows：

```cmd
cd
dir
```

应该能看到：

```text
manage.py
```

---

# 10. Django 端口 8000 被占用

现象：

```text
Error: That port is already in use.
```

可以临时：

```bash
python manage.py runserver 8001
```

但注意：

如果后端改成 8001，前端：

```text
frontend/src/js/config/config.js
```

也必须对应修改 HTTP_URL。

---

# 11. Vite 端口 5173 被占用

Vite 可能自动改到：

```text
5174
```

此时 Django CORS 仍只允许：

```text
http://localhost:5173
```

解决方式之一：

- 关闭占用 5173 的进程；或
- 修改 `CORS_ALLOWED_ORIGINS` 增加新端口。

---

# 12. 浏览器报 CORS

典型 Console：

```text
blocked by CORS policy
```

检查：

```text
backend/backend/settings.py
```

当前：

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

确认浏览器实际地址是不是：

```text
http://localhost:5173
```

注意：

```text
localhost
```

和：

```text
127.0.0.1
```

在 Origin 判断里可能被视为不同来源。

---

# 13. 页面能开，但 API 404

F12 → Network。

检查 Request URL。

后端 API 路由总表：

```text
backend/web/urls.py
```

例如聊天必须是：

```text
/api/friend/message/chat/
```

Django 默认常常区分末尾 `/`。

---

# 14. API 401 Unauthorized

先判断：

```text
没有登录？
access token 没带？
access token 过期？
refresh token 也过期？
```

F12 → Network → Request Headers。

应该能看到：

```http
Authorization: Bearer xxxxx
```

如果没有，检查：

```text
frontend/src/stores/user.js
frontend/src/js/http/api.js
```

---

# 15. 普通 Axios 能刷新 token，但 SSE 401

SSE 走的是：

```text
frontend/src/js/http/streamApi.js
```

不是普通 Axios 调用。

检查它的：

```text
onopen(response)
onerror(err)
```

以及：

```text
Authorization
```

header。

---

# 16. 注册/登录后页面仍认为没登录

检查 Pinia：

```text
frontend/src/stores/user.js
```

特别看：

```text
accessToken
hasPulledUserInfo
```

再看 router guard：

```text
frontend/src/router/index.js
```

新手常见问题是：

> API 登录成功了，但状态没有同步到 Pinia。

---

# 17. Django 500 Internal Server Error

不要猜。

看运行：

```bash
python manage.py runserver
```

那个终端中的 traceback。

从 traceback 最底部往上看：

```text
异常类型
错误信息
你自己的文件路径
行号
```

例如：

```text
KeyError: 'friend_id'
```

那就去看请求 payload 是否包含 `friend_id`。

---

# 18. `no such table`

例如：

```text
OperationalError: no such table: ...
```

通常没有迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

如果仓库已经包含 migration，一般只需要：

```bash
python manage.py migrate
```

---

# 19. 上传头像 / 背景后图片打不开

检查：

```text
backend/backend/settings.py
```

开发模式 MEDIA_URL：

```text
http://127.0.0.1:8000/media/
```

并确认：

```text
backend/media/
```

有文件。

再检查后端是否以 DEBUG 开发模式运行。

---

# 20. `.env` 写了但 `os.getenv()` 还是 None

先确保变量名完全一致：

```env
API_KEY=...
API_BASE=...
WSS_URL=...
```

不要写成：

```env
OPENAI_API_KEY=...
```

除非你同步修改代码。

然后在激活 venv 后测试：

```bash
cd backend
python manage.py shell
```

```python
import os
print(os.getenv('API_KEY'))
print(os.getenv('API_BASE'))
print(os.getenv('WSS_URL'))
```

如果打印 `None`，说明 `.env` 没被加载或路径/文件名有问题。

确认文件真的是：

```text
.env
```

而不是 Windows 隐藏扩展名导致：

```text
.env.txt
```

---

# 21. LLM 401 / 403

这通常不是 Django JWT 401，而是模型服务商返回。

检查：

```text
API_KEY
API_BASE
```

以及你的账号是否有对应模型权限。

当前聊天模型名写在：

```text
backend/web/views/friend/message/chat/graph.py
```

记忆模型在：

```text
backend/web/views/friend/message/memory/graph.py
```

如果服务商不支持这个模型名，需要改成你有权限的模型。

---

# 22. `model not found`

原因：模型名是供应商相关的。

当前项目不是“任何 OpenAI-compatible 服务填 URL 就一定能跑”。

兼容的是调用协议，不代表模型名统一。

检查服务商实际提供：

```text
聊天模型
Embedding 模型
ASR 模型
TTS 模型
```

并分别修改项目配置/代码。

---

# 23. 文本聊天可以，Embedding 报错

因为聊天与 Embedding 是两次不同 API。

文件：

```text
backend/web/documents/utils/custom_embeddings.py
```

当前 Embedding 模型：

```text
text-embedding-v4
```

并请求：

```text
dimensions=1024
```

你的服务商必须支持对应模型和参数。

---

# 24. RAG 查询时报 LanceDB 表不存在

先确认你构建过知识库。

创建：

```text
backend/web/documents/data.txt
```

然后：

```bash
cd backend
python manage.py shell
```

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

检查目录：

```text
backend/web/documents/lancedb_storage
```

---

# 25. `data.txt` 不存在

它被 `.gitignore` 故意忽略。

这不是仓库漏传。

请自己创建：

```text
backend/web/documents/data.txt
```

放你的知识库内容。

---

# 26. RAG 有库但模型从不调用 Tool

检查 Tool docstring：

```text
backend/web/views/friend/message/chat/graph.py
```

当前描述比较专用，强调“阿里云百炼平台”。

如果你问的是完全无关领域，模型可能认为不应该调用。

可以把工具描述改成你的知识库用途，例如：

```text
当用户问题需要查询项目私有知识库时调用此工具。
```

---

# 27. Tool 执行后没有最终回答

检查 LangGraph：

```text
agent
 ↓
tools
 ↓
agent
```

关键是：

```python
graph.add_edge('tools', 'agent')
```

Tool 结果需要再次交给模型生成自然语言回答。

---

# 28. LangGraph 报 `tool_calls` 相关错误

先打印/检查最后一条 message 类型和模型是否支持 tool calling。

并确认：

```python
llm = ChatOpenAI(...).bind_tools(tools)
```

不是普通未绑定工具的模型。

某些“兼容 OpenAI”的第三方模型未必完整兼容 Tool Calling。

---

# 29. SSE 返回的不是 `text/event-stream`

前端 `streamApi.js` 会检查 content-type。

后端聊天应该返回：

```python
StreamingHttpResponse(..., content_type="text/event-stream")
```

如果你误把它改成：

```python
Response(...)
```

前端会认为不是流式接口。

---

# 30. SSE 在代理/Nginx 后变成“一次性全部出现”

常见原因：代理缓冲。

项目后端已经设置：

```text
X-Accel-Buffering: no
Cache-Control: no-cache
```

生产部署时仍需要检查反向代理配置，确保 SSE 不被缓存/缓冲。

---

# 31. SSE 文本能显示，但页面刷新后聊天不见了

检查 `Message.objects.create(...)` 是否执行。

在 Admin：

```text
/admin/
```

看 Message 表是否产生记录。

如果没有，检查流生成器是否异常提前退出。

---

# 32. 长期记忆一直为空

先确认：

```text
Message 数量是否达到 5 的倍数？
```

当前触发：

```python
count() % 5 == 0
```

再检查 Admin 中：

```text
SystemPrompt title='记忆'
```

是否有合理 prompt。

最后检查 MemoryGraph 的模型 API 是否能正常调用。

---

# 33. 长期记忆更新后“胡编”

这是 prompt / 模型质量问题，不是数据库 bug。

建议记忆 prompt 明确：

```text
只保存对未来对话有帮助的稳定事实
不推断用户未说过的信息
不把一次性情绪当永久事实
遇到冲突以最近明确陈述为准
```

更进一步可以把记忆改成结构化 JSON。

---

# 34. ASR 报 WebSocket 连接失败

检查：

```env
WSS_URL=...
API_KEY=...
```

再判断：

```text
DNS？
TLS？
Authorization？
服务端模型权限？
WebSocket 地址是否正确？
```

ASR 与普通 HTTP API 不是同一连接。

---

# 35. ASR 返回空字符串

检查：

```text
上传音频真的是 PCM？
sample_rate 是否 16000？
服务端事件是否 result-generated？
sentence_end 是否出现？
```

当前代码只在：

```text
sentence_end == true
```

时追加 transcription。

---

# 36. TTS 没声音但文本正常

先分层：

```text
LLM 文本正常
  ↓
TTS sender 有发送吗？
  ↓
TTS receiver 有 bytes 吗？
  ↓
SSE 有 audio 字段吗？
  ↓
浏览器有收到吗？
  ↓
MediaSource 能播放吗？
```

不要直接认定是前端播放器。

---

# 37. Character 没有 Voice 导致聊天异常

聊天线程当前会读取：

```text
friend.character.voice.voice_id
```

所以没有 Voice 时可能发生空引用。

新手第一次复刻：

1. Admin 创建 Voice；
2. 创建 Character 时选择 Voice；
3. 再测试 TTS。

未来工程优化建议：支持 voice 为空时自动进入 text-only 模式。

---

# 38. 浏览器提示音频自动播放被阻止

现代浏览器常限制没有用户交互的 autoplay。

项目已有：

```js
audioPlayer.play().catch(...)
```

尽量确保播放由用户“点击发送/麦克风”等手势触发。

---

# 39. `MediaSource.addSourceBuffer('audio/mpeg')` 报错

可能是：

```text
浏览器不支持该 MIME
TTS 实际返回格式不是 MP3
数据流不是可追加的 MP3 格式
```

检查服务端 TTS 参数：

```text
format: mp3
```

再检查浏览器兼容性。

---

# 40. 音频断断续续

检查：

```text
网络延迟
TTS chunk 产生速度
audioQueue 是否经常为空
SourceBuffer 是否报错
文本 chunk 是否太碎
```

当前代码几乎把每个 LLM content chunk 都推给 TTS。

生产优化可以考虑按：

```text
标点
句子
固定字符数
```

聚合后再发 TTS，减少碎片。

---

# 41. `websockets.connect` 参数报错

Websockets 库不同大版本 API 可能变化。

项目已固定：

```text
websockets==15.0.1
```

不要随手：

```bash
pip install -U websockets
```

升级后如果 API 变化，代码可能不兼容。

整个项目 requirements 已经 pin 版本，初次复刻请优先按锁定版本安装。

---

# 42. 为什么不建议新手先升级所有依赖？

因为：

```text
教程代码
  ↕
特定版本 API
```

如果你一上来：

```bash
pip install -U everything
npm update
```

你调试的就不再是 AiFriends，而是“框架升级兼容问题”。

正确顺序：

```text
先按锁定版本跑通
   ↓
再一个依赖一个依赖升级
```

---

# 43. 页面 404，但直接访问首页正常

Vue 使用 history router。

刷新：

```text
/friend
```

时浏览器会把 `/friend` 请求交给服务器。

后端需要 fallback 到前端 index。

项目 `web/urls.py` 已有 `re_path` fallback。

生产部署到 Nginx 时也要做 SPA fallback。

---

# 44. 如何判断是前端还是后端问题？

最简单方法：看 Network。

## 没发请求

大概率前端。

## 发了请求但 4xx/5xx

看后端/认证/请求数据。

## 后端返回正确，但 UI 不变

大概率 Vue 状态更新/组件逻辑。

## SSE Network 一直有数据，但页面不更新

检查 `onmessage` 与 emit。

---

# 45. 如何最小化问题？

如果完整聊天不工作，按这个顺序拆：

```text
1. Django 返回固定 JSON
2. Django 返回固定 SSE
3. 前端能显示固定 SSE
4. LLM 非流式调用
5. LLM 流式调用
6. LangGraph 无 Tool
7. 加 get_time Tool
8. 加 RAG Tool
9. 加 TTS
```

每一步成功再加下一层。

这叫：

> 减少变量。

---

# 46. 推荐保存的诊断信息

提 Issue 或问别人时，不要只发：

```text
“为什么跑不了？”
```

请提供：

```text
操作系统：Windows 11 / macOS / Ubuntu
Python：python --version
Node：node -v
当前命令：...
浏览器 URL：...
HTTP 状态码：...
后端 traceback：...
前端 Console：...
修改过哪些文件：...
```

API Key 必须打码。

---

# 47. 一个通用排查模板

```text
【我要做什么】
例如：发送聊天消息

【预期结果】
AI 流式输出

【实际结果】
HTTP 500

【前端 Console】
...

【Network】
Request URL:
Status:
Payload:
Response:

【Django traceback】
...

【环境】
Python:
Node:
OS:

【我已经尝试】
...
```

这个模板能极大提高别人帮你定位问题的速度。

---

# 48. 最后原则：一次只改一层

错误调试最怕：

```text
同时改前端
同时改后端
同时换模型
同时升级依赖
同时换数据库
```

最后即使好了，你也不知道为什么好。

推荐：

```text
复现
 ↓
定位层级
 ↓
做一个最小改动
 ↓
重新测试
 ↓
commit
```

这就是从“新手试错”走向“工程调试”的第一步。
