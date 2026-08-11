# Chapter 09 Lab：长期记忆——把不断增长的聊天压缩成 Friend.memory

## 本章目标

解决一个真实问题：

```text
聊天轮数越来越多
  ↓
如果把全部历史永远塞进 prompt
  ↓
上下文越来越长、越来越贵、越来越慢
```

本章实现两层记忆：

```text
短期记忆：最近若干 Message
长期记忆：Friend.memory 中的压缩摘要
```

---

## 历史检查点

```text
15a8a8427db9801f1fcc01da5d15cfdb97014111  添加长期记忆
```

最终项目后来把触发频率调整为每 5 条 Message 更新一次。

---

## TODO 1：先做“没有长期记忆”的成本实验

创建 20 轮聊天记录。

临时打印每次发送给 LLM 的 messages 数量与序列化长度。

记录：

```text
第 1 轮：
第 5 轮：
第 10 轮：
第 20 轮：
```

回答：如果继续无限追加，成本会发生什么？

---

## TODO 2：理解 `Friend.memory`

为什么 memory 放在：

```text
Friend
```

而不是：

```text
Character
```

因为：

```text
用户 A ↔ Alice Character：记忆 A
用户 B ↔ Alice Character：记忆 B
```

Character 是共享角色设定；Friend.memory 是关系私有状态。

---

## TODO 3：创建 Memory Prompt

Admin 中添加：

```text
title='记忆'
order_number=1
prompt='请根据原始记忆与最近对话，更新一份简洁且事实准确的长期记忆...'
```

要求提示词至少约束：

- 保留稳定事实
- 删除无价值寒暄
- 不凭空编造
- 新事实可以覆盖旧的过时事实
- 输出长度受控

---

## TODO 4：构造 Memory Graph 输入

System：

```python
SystemMessage(memory_prompt)
```

Human：

```text
[原始记忆]
{friend.memory}

[最近对话]
user: ...
ai: ...
```

### 验收

打印最终 inputs，确认它不是把数据库对象直接塞给模型，而是转换成清晰文本/Message。

---

## TODO 5：最小 MemoryGraph

这一张图故意很简单：

```text
START → agent → END
```

为什么不需要 ToolNode？

因为当前记忆更新任务只是：

> 给定旧记忆和最近聊天，让 LLM 生成新的压缩记忆。

它不需要外部工具循环。

---

## TODO 6：更新 `Friend.memory`

模型返回后：

```python
friend.memory = res['messages'][-1].content
friend.update_time = now()
friend.save()
```

### 验收

在 Admin 中观察：

```text
Friend.memory
```

随着聊天变化，但长度不会无限等比例增长。

---

## TODO 7：触发频率

先尝试每一条 Message 都更新记忆。

记录：

- 模型调用次数
- 延迟
- token 成本

再改成：

```python
if Message.objects.filter(friend=friend).count() % 5 == 0:
    update_memory(friend)
```

### 思考

这是一种简单触发策略，不是唯一最佳方案。

可能的改进：

- 每 N 轮
- 达到 token 阈值
- 异步后台任务
- 仅当检测到新事实时更新

---

## TODO 8：把长期记忆重新喂回聊天

在普通聊天 SystemMessage 中追加：

```text
[长期记忆]
{friend.memory}
```

然后测试：

1. 告诉 AI：“我最喜欢的颜色是绿色。”
2. 继续聊足够轮数触发 Memory 更新
3. 新开/继续对话问：“我喜欢什么颜色？”

### 验收

AI 能利用 memory 回答，而不必始终把最早的原始消息留在短期窗口中。

---

## 主动错误实验：记忆污染

故意使用一个非常宽松的 Memory Prompt，例如：

```text
请自由总结并补充你认为有用的信息。
```

观察是否可能产生不存在的“事实”。

然后收紧 Prompt。

理解：

> 长期记忆不是普通摘要。错误事实一旦被压缩保存，会在未来很多轮中反复影响模型。

---

## 参考答案思路

记忆更新其实是一个有状态的压缩函数：

```text
new_memory = f(old_memory, recent_messages)
```

它追求的不是“完整保存所有字”，而是：

```text
稳定事实 + 用户偏好 + 重要关系 + 未完成事项
```

同时丢掉：

```text
大量重复寒暄 + 无长期价值的逐字对话
```

---

## 常见错误

### memory 一直空

检查触发条件是否达到，`update_memory()` 是否实际执行。

### memory 更新后聊天里没效果

你保存了 memory，但没有在 `add_system_prompt()` 中重新放回上下文。

### 每次回复越来越慢

可能在同步请求结束前执行了额外 Memory LLM 调用。思考是否要异步化。

### AI 记住了错误信息

检查记忆 Prompt、输入顺序和旧 memory 是否已经被污染。

---

## Challenge

设计一个“结构化记忆”格式：

```json
{
  "user_profile": {},
  "preferences": [],
  "important_events": [],
  "open_tasks": []
}
```

不要求正式改项目，但写出：

1. 它比自由文本 memory 的优点
2. 它的缺点
3. 如何让 LLM 安全更新其中一个字段而不破坏其它字段
