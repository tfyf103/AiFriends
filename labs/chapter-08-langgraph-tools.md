# Chapter 08 Lab：SystemPrompt、多轮上下文与 LangGraph Tool Calling

## 本章目标

把“模型直接回答”升级成真正的最小 Agent：

```text
START
  ↓
agent
  ├─ 不需要工具 → END
  └─ tool_calls
       ↓
     ToolNode
       ↓
     agent 再思考
```

同时让角色拥有：

- SystemPrompt
- Character Profile
- 最近多轮对话
- 工具调用

---

## 历史检查点

```text
3bcc4a8c8e169475af6c78b2ac19752b62625bdf  系统提示词与多轮上下文
72c4c3ae5efb950e7b4f08cded3a37238e961c78  Function/Tool Calling
```

---

## TODO 1：先理解三类 Message

自己构造：

```python
SystemMessage('你是一个耐心的老师')
HumanMessage('1+1是多少？')
AIMessage('2')
```

回答：

- SystemMessage 为什么不等于普通用户输入？
- 历史 AI 回复为什么要用 AIMessage，而不是再次用 HumanMessage？

### 验收

你能画出：

```text
System
Human(old)
AI(old)
Human(current)
```

---

## TODO 2：数据库驱动 SystemPrompt

在 Admin 创建：

```text
title='回复'
order_number=1
prompt='...'
```

后端按 `order_number` 拼接。

然后追加：

```text
[角色性格]
{friend.character.profile}
```

### 验收

不改 Python 源码，仅修改 Admin 中的 SystemPrompt，模型行为就能变化。

理解这叫：

> 把可运营配置从代码中分离出来。

---

## TODO 3：加入最近 10 条历史

查询：

```python
Message.objects.filter(friend=friend).order_by('-id')[:10]
```

注意拿到的是“从新到旧”，但对话上下文应该“从旧到新”。

所以：

```python
message_raw.reverse()
```

再映射：

```text
Message.user_message → HumanMessage
Message.output       → AIMessage
```

### 主动错误实验

故意不 reverse，让最近对话逆序进入模型，观察多轮回答是否更混乱。

---

## TODO 4：创建第一个 Tool

```python
@tool
def get_time() -> str:
    """当需要查询精确时间时调用。"""
    ...
```

### 必须理解

`@tool` 不等于“模型已经会执行这个函数”。

它只是把：

- 名字
- 参数 schema
- docstring 描述

提供给模型/框架。

---

## TODO 5：`bind_tools()`

```python
llm = ChatOpenAI(...).bind_tools(tools)
```

测试：

```text
用户：现在的精确时间是多少？
```

观察 LLM Message 是否产生：

```text
tool_calls
```

### 关键问题

如果只有 `bind_tools()`，但没有真正执行工具，会发生什么？

答案：模型最多提出“我要调用工具”，不会自动帮你执行任意 Python 函数。

---

## TODO 6：建立 StateGraph

State：

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

节点：

```text
agent
tools
```

边：

```text
START → agent
agent → tools 或 END
tools → agent
```

### 验收

你必须能手动画图，不看源码解释每条边为什么存在。

---

## TODO 7：Conditional Edge

实现：

```python
def should_continue(state):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tools'
    return 'end'
```

然后：

```python
graph.add_conditional_edges(...)
```

### 主动错误实验

暂时删除：

```text
tools → agent
```

观察工具执行后为什么无法生成自然语言最终答案。

---

## TODO 8：观察完整 Tool Calling Message 序列

临时打印/调试：

```text
HumanMessage
AIMessage(tool_calls=[...])
ToolMessage(result=...)
AIMessage(final answer)
```

### 验收

能解释：

> Tool 的返回值不是直接展示给用户；它通常回到 Agent，让 LLM 基于工具结果生成最终语言回复。

---

## 参考答案思路

LangGraph 在这里解决的不是“让 LLM 更聪明”，而是**明确控制执行流程**：

```text
模型思考
  ↓
是否需要外部动作？
  ├─ 否 → 返回
  └─ 是 → Python Tool
             ↓
         ToolMessage
             ↓
         模型再次思考
```

---

## 常见错误

### Tool 从来不触发

检查：

- docstring 是否描述清楚使用场景
- tools 是否真的传给 `bind_tools`
- 用户问题是否需要该工具

### `last_message.tool_calls` 不存在

确认最后一条确实是支持 tool_calls 的 AI message 类型。

### 工具无限循环

模型一直请求工具，或者路由逻辑/工具返回值不能帮助模型完成任务。需要观察完整 state，而不是只看最终 UI。

### State 中历史越来越怪

检查 `add_messages` 的 reducer 以及你传入 state 的 message 顺序。

---

## Challenge

新增一个纯本地 Tool：

```python
@tool
def calculate_rectangle_area(width: float, height: float) -> float:
    ...
```

要求：

1. 问普通闲聊时不调用
2. 问矩形面积时调用
3. Tool 返回数字
4. LLM 最后用自然语言回答

然后写一段文字解释：为什么确定性计算适合 Tool，而不应让模型“凭语言感觉”算。
