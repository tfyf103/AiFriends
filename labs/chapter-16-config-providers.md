# Chapter 16 Lab：配置、Feature Flag 与多模型供应商

## 本章目标

把“改源码才能换模型”升级成“运行时配置决定能力”。

第四轮新增：

```text
backend/web/ai/config.py
.env.example
```

并提供：

```text
AI_MODE=mock | text | full
ENABLE_RAG
ENABLE_ASR
ENABLE_TTS
CHAT_MODEL
MEMORY_MODEL
EMBEDDING_MODEL
ASR_MODEL
TTS_MODEL
```

---

## TODO 1：体验三个模式

### Mock

```env
AI_MODE=mock
```

要求：不填真实 API Key 也能完成登录、Friend、SSE Chat、Message 落库。

### Text

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

要求：真实 LLM 可以聊天，但不需要语音服务。

### Full

逐项开启：

```env
ENABLE_RAG=true
ENABLE_ASR=true
ENABLE_TTS=true
```

不要一次全开；每打开一个能力都运行 `doctor`。

---

## TODO 2：运行 doctor

```bash
cd backend
python manage.py doctor
```

故意删除一个配置，再观察输出。

要求你解释：

```text
required failure
optional warning
```

为什么应该区分。

---

## TODO 3：模型名不能散落源码

搜索：

```text
deepseek-v4-pro
text-embedding-v4
gummy-realtime-v1
cosyvoice-v3-flash
```

检查是否都通过 `get_ai_settings()` 获取。

---

## TODO 4：设计 Provider Adapter

下一步不要让业务层知道某个具体厂商。

设计接口：

```python
class ChatProvider:
    def create_model(self): ...

class EmbeddingProvider:
    def embed_documents(self, texts): ...
```

思考 OpenAI-compatible 能统一什么，不能统一什么：

```text
HTTP schema 可能兼容
模型名不兼容
Tool Calling 兼容程度不同
stream usage metadata 不一定相同
ASR/TTS WebSocket 协议通常不同
```

---

## TODO 5：Feature Flag 测试

自动验证：

```text
mock 不调用 ChatOpenAI
text 默认不连接 WSS
ENABLE_RAG=false 不注册知识库 Tool
ENABLE_ASR=false 返回清楚的 503
ENABLE_TTS=false 仍能真实文本聊天
```

---

## 验收

- [ ] 三个模式都能解释；
- [ ] 能用 doctor 找到缺失配置；
- [ ] 新增模型不需要修改 5 个业务文件；
- [ ] 能说明 feature flag 与用户权限不是同一个概念；
- [ ] 能说明配置文件为什么不能包含真实 Secret。

---

## Challenge

加入第四种 provider，例如本地 Ollama / 另一个 OpenAI-compatible 服务，并做到：

```text
业务 View 不改
LangGraph 拓扑不改
只增加 provider/config 层
```
