# Chapter 20 Lab：CI、Build、Deploy 与 Observability

## 本章目标

把“我电脑上能跑”升级成：

> **每次改动有人自动检查，构建结果可重复，线上出错时能定位。**

---

## TODO 1：读懂 GitHub Actions

文件：

```text
.github/workflows/ci.yml
```

当前至少检查：

```text
Python compile
Django check
Django tests
npm ci
VAD asset setup
frontend quality check
Node tests
Vite build
```

要求你能解释：

```text
为什么 CI 使用 AI_MODE=mock？
为什么不能让每个 PR 都消耗真实 LLM/TTS 额度？
```

---

## TODO 2：故意让 CI 失败

任选：

```text
破坏 singleFlight test
写一处 trailing whitespace
引入 Python syntax error
删掉一个 import
```

推到学习分支，观察 GitHub Actions。

修复后再看绿灯。

---

## TODO 3：Build 不等于 Dev Server

开发：

```bash
npm run dev
```

构建：

```bash
npm run build
```

第四轮已打开：

```js
manifest: true
```

Django 使用 Vite manifest 查找真实 hash 资源，而不是硬编码：

```text
index-xxxx.js
index-yyyy.css
```

解释为什么 hash 每次可能变化。

---

## TODO 4：Health Check

新增：

```text
GET /api/health/
```

建议分层：

```json
{
  "status": "ok",
  "database": "ok",
  "ai_mode": "text",
  "rag": "disabled",
  "speech": "disabled"
}
```

不要在公开 health endpoint 暴露：

```text
API Key
内部异常堆栈
私人配置
```

---

## TODO 5：结构化日志

为一次聊天建立：

```text
request_id
user_id
friend_id
ai_mode
model
rag_used
cancelled
input_tokens
output_tokens
latency_ms
error_type
```

要求一条请求从 Django 到 AI worker 能用同一个 request_id 串起来。

---

## TODO 6：基础指标

至少思考：

```text
请求量
4xx / 5xx
LLM latency
首 token latency
TTS 首包 latency
取消率
Token / request
RAG tool call rate
Memory update failure rate
```

不要一开始追求复杂平台；先学会“什么值得测”。

---

## TODO 7：Docker 学习版

自己编写一个多阶段 Dockerfile：

```text
Node stage → npm ci → npm run build
Python stage → pip install → copy backend/static/frontend
```

第一次只要求：

```text
docker build 成功
容器能启动 Django
```

然后再讨论：

```text
runserver 为什么不是生产 WSGI/ASGI server？
static/media 谁负责？
数据库为什么不能永远 SQLite？
Secret 怎么注入？
```

---

## TODO 8：部署前检查

建立 checklist：

```text
DEBUG=false
SECRET_KEY 来自环境变量
ALLOWED_HOSTS
HTTPS
Secure Cookie
CORS/CSRF
数据库 migration
static collect/build
media 持久化
日志
备份
rate limit
health check
```

---

## 验收

- [ ] PR 会自动跑 CI；
- [ ] 能故意制造一次红灯并修复；
- [ ] 能解释 Vite manifest；
- [ ] 有 health endpoint；
- [ ] 有 request_id；
- [ ] 至少记录 latency / token / error；
- [ ] 能构建一个学习版 Docker image；
- [ ] 能说清“开发服务器”和“生产部署”的区别。

---

## 最终毕业任务

从 Chapter 00 开始任选一个功能，例如：

```text
RAG 来源引用
结构化 Memory
角色级知识库
停止生成
```

要求完整提交：

```text
需求说明
架构图
代码
数据库变更
API 文档
自动测试
CI 绿灯
安全分析
性能指标
故障排查说明
```

做到这里，你已经不是在“跟教程敲代码”，而是在完成一个小型真实软件工程项目。
