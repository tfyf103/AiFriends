# Chapter 19 Lab：RAG Evaluation、来源引用与结构化 Memory

## 本章目标

把“RAG 能搜到东西、Memory 能生成一段摘要”升级成：

> **我能测量它是否真的更准，而且知道每条记忆/资料来自哪里。**

---

## TODO 1：建立最小 RAG 评测集

创建：

```text
evals/rag_cases.json
```

每条至少包含：

```json
{
  "question": "AiFriends 使用什么向量数据库？",
  "expected_keywords": ["LanceDB"],
  "expected_source": "data.txt#..."
}
```

至少准备 20 条：

```text
10 条应该命中知识库
5 条不应该命中
5 条容易混淆
```

---

## TODO 2：检索与生成分开评测

不要只看最终答案。

拆成：

```text
Retrieval
  ↓
是否找对 chunk？

Generation
  ↓
是否忠于 chunk？
```

指标可以从简单开始：

```text
Recall@k
关键词命中
source 命中
人工 faithfulness 评分
```

---

## TODO 3：返回来源

当前 Tool 主要返回纯文本。

升级 Document metadata：

```json
{
  "source": "guide.md",
  "chunk_id": "guide-003"
}
```

让最终 UI 能展示：

```text
参考资料：guide.md / chunk 003
```

要求来源来自检索结果，不允许 LLM 自己编一个 citation。

---

## TODO 4：结构化长期记忆

当前：

```text
Friend.memory = 一段自由文本
```

设计 JSON：

```json
{
  "profile": [],
  "preferences": [],
  "relationships": [],
  "goals": [],
  "events": []
}
```

每条记忆增加：

```text
value
source_message_id
timestamp
confidence
status
```

---

## TODO 5：Memory 冲突

模拟：

```text
Day 1：我最喜欢咖啡
Day 10：我现在不喝咖啡了，改喝茶
```

设计策略：

```text
覆盖旧值？
保留历史？
标记 superseded？
让模型自行总结？
```

要求最终结果能解释“为什么当前记忆是茶”。

---

## TODO 6：Memory Eval

准备测试对话：

```text
稳定偏好
短期情绪
一次性事件
冲突事实
否定句
敏感信息
```

评估：

```text
该记的是否记了？
不该记的是否没记？
冲突是否更新？
有没有虚构？
```

---

## TODO 7：成本与效果一起看

记录：

```text
retrieval latency
embedding latency
LLM latency
input tokens
output tokens
memory update tokens
```

比较：

```text
k=3 vs k=5
chunk_size=300 vs 500 vs 800
每 5 条更新 memory vs 每 10 条
```

---

## 验收

- [ ] 有固定 RAG eval set；
- [ ] retrieval 与 generation 分开评测；
- [ ] UI/响应能看到真实 source；
- [ ] Memory 有结构化 schema；
- [ ] 能处理至少一种冲突；
- [ ] 有“不该记”的测试；
- [ ] 能用数据比较两套 RAG/Memory 参数。

---

## Challenge

做一个开发页：

```text
RAG Debug Panel
```

显示：

```text
query
query vector dimensions
top-k chunks
similarity score
source
最终 prompt
最终 answer
latency / token
```

把 RAG 从“黑箱”变成可观察系统。
