# AiFriends 工程进阶课程：Chapter 14–20

> Chapter 00–13 回答：“我能不能从 0 做出一个 AI 全栈应用？”
>
> Chapter 14–20 回答：“我能不能把一个能跑的 AI Demo 变成可测试、可维护、可部署、可观察的工程项目？”

---

## 课程地图

| Chapter | 主题 | 当前项目中的真实锚点 |
|---|---|---|
| 14 | Testing / TDD | `backend/web/tests.py`、`frontend/tests/`、`.github/workflows/ci.yml` |
| 15 | DRF 工程化 | account / character / friend API 的 validation 与 status code |
| 16 | 配置与多模型 | `backend/web/ai/config.py`、`.env.example` |
| 17 | 异步、流与取消 | `AbortController`、SSE、`cancel_event`、Queue、WebSocket |
| 18 | 数据与安全 | Friend 唯一关系、Transaction、文件上传、隐私、Prompt Injection |
| 19 | RAG / Memory 评测 | LanceDB、引用来源、结构化记忆、冲突策略、eval set |
| 20 | CI / Build / Deploy / Observability | GitHub Actions、Vite manifest、health/logging/metrics |

对应实验：[`../labs/README.md`](../labs/README.md)。

---

## 为什么课程要有第二阶段？

很多 AI 教程停在：

```text
能注册
能聊天
能 RAG
能语音
```

但真正的工程问题通常从这里才开始：

```text
谁证明改动没把登录弄坏？
多个 401 为什么只刷新一次 token？
语音服务挂了，文本为什么也不能聊？
用户点“停止”后模型是否真的停止？
RAG 回答引用了哪条资料？
Memory 新旧事实冲突怎么办？
构建后的 hash 文件名为什么会变化？
线上报错怎么知道发生在哪一层？
```

Chapter 14–20 就围绕这些问题训练。

---

## 推荐学习方式

每章都使用同一个循环：

```text
1. 先复现一个工程问题
2. 写一个失败测试 / 明确验收条件
3. 做最小重构
4. 让测试通过
5. 观察日志、网络或数据库证据
6. 写 ADR/学习笔记解释 trade-off
7. commit
```

不要一次把项目“重构得很漂亮”。工程训练的重点是：每一次改动都能被解释、验证和回滚。

---

## 第四轮已经给出的参考实现

这一轮主线候选代码已经提供几个可直接学习的工程模式：

- `mock / text / full` 三种 AI 运行模式；
- Chat / Memory / Embedding / ASR / TTS 模型名环境变量化；
- TTS 可关闭，真实文本聊天不再依赖语音 WebSocket；
- Axios 与 SSE 共用一个 single-flight refresh；
- `AbortController` 关闭真实 SSE，后端 `cancel_event` 尽快停止 worker；
- `manage.py doctor` 环境自检；
- `manage.py seed_demo` 幂等初始化教学数据；
- `npm run setup:vad` 自动准备 VAD/ONNX Runtime 资源；
- Django/Node 自动测试；
- GitHub Actions；
- Vite manifest 驱动 Django 模板，不再硬编码 hash 文件名。

这些不是“最终架构”，而是从 Demo 进入工程化的第一层参考答案。

---

## 毕业标准

完成 Chapter 20 后，你应该能独立回答：

- 单元测试、集成测试、端到端测试分别保护什么？
- 为什么 HTTP status code 和业务 `result` 不应该混成一团？
- Serializer 为什么比到处 `request.data.get(...).strip()` 更适合复杂 API？
- 为什么配置、模型供应商和业务代码要解耦？
- SSE/LLM/TTS 的取消信号怎样跨线程/协程传播？
- 为什么数据库唯一约束不能被“先查再 create”替代？
- Prompt Injection 与普通 Web 权限漏洞有什么区别？
- RAG 如何建立可重复的评测集，而不是凭感觉说“效果不错”？
- Memory 如何表达来源、时间、置信度和冲突？
- CI 为什么必须在 PR 合并前运行？
- Build、Deploy、Runtime Observability 是三件什么不同的事？

做到这里，你学到的就不只是 AiFriends，而是一套可迁移到其他 AI 产品的工程方法。
