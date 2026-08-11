# Chapter 08 Lab: SystemPrompt, Multi-turn Context, and LangGraph Tool Calling

🌐 **Language:** [简体中文](../chapter-08-langgraph-tools.md) | **English**

## Goal

Upgrade “the model answers directly” into a minimal Agent with an explicit execution loop:

```text
START
  ↓
agent
  ├─ no tool needed → END
  └─ tool_calls
       ↓
     ToolNode
       ↓
     agent reasons again
```

At the same time, the character should receive:

- operational `SystemPrompt` content;
- `Character.profile` persona data;
- recent multi-turn conversation history;
- controlled Tool Calling.

---

## Historical checkpoints

Useful project-history commits:

```text
3bcc4a8c8e169475af6c78b2ac19752b62625bdf  system prompt + multi-turn context
72c4c3ae5efb950e7b4f08cded3a37238e961c78  function/tool calling
```

Use them to study how the architecture evolved, then compare with the current graph implementation.

---

## TODO 1: Understand the message types first

Construct a tiny sequence:

```python
SystemMessage('You are a patient teacher.')
HumanMessage('What is 1 + 1?')
AIMessage('2')
```

Answer:

- Why is a `SystemMessage` not just another user message?
- Why should a previous assistant reply become `AIMessage` instead of another `HumanMessage`?

### Acceptance

You can draw and explain:

```text
System
Human(previous)
AI(previous)
Human(current)
```

The message role is part of the model input semantics, not cosmetic metadata.

---

## TODO 2: Make SystemPrompt operational data

AiFriends stores prompt fragments in the database so maintainers can change operational prompt configuration without editing Python source code.

Create or inspect a prompt record such as:

```text
title='回复'
order_number=1
prompt='...'
```

Then conceptually append character persona information:

```text
[Character persona]
{friend.character.profile}
```

### Acceptance

Change the prompt in Django Admin and verify that behavior can change without modifying the graph code.

Explain the engineering idea:

> Operational configuration that needs to evolve independently can be separated from hard-coded business logic.

---

## TODO 3: Add recent conversation history

A typical query is conceptually:

```python
Message.objects.filter(friend=friend).order_by('-id')[:10]
```

This returns newest-first data, while model context should usually be chronological.

So reverse the selected rows before mapping them into:

```text
Message.user_message → HumanMessage
Message.output       → AIMessage
```

### Deliberate failure

Temporarily skip the reverse step.

Observe how reversed conversational chronology can make multi-turn behavior less coherent.

Restore the correct order.

### Acceptance

You can explain the difference between:

```text
SQL retrieval order
vs
conversation semantic order
```

---

## TODO 4: Create your first Tool

Example:

```python
@tool
def get_time() -> str:
    """Use this when the exact current time is required."""
    ...
```

### Must understand

`@tool` does **not** mean the model automatically executes the Python function.

It exposes information such as:

- tool name;
- parameter schema;
- docstring/description;
- callable implementation for the framework.

The model can propose a tool call; the application still controls whether and how it executes.

---

## TODO 5: Bind tools to the model

Conceptually:

```python
llm = ChatOpenAI(...).bind_tools(tools)
```

Ask something like:

```text
What is the exact current time?
```

Inspect the returned AI message for:

```text
tool_calls
```

### Critical question

What happens if you call `bind_tools()` but never execute the requested tool?

The model can at most emit a structured request saying “I want this tool.” It cannot magically run arbitrary application Python by itself.

---

## TODO 6: Define Agent state

A minimal state can look like:

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

The important idea is that graph nodes exchange explicit state.

For this Agent, the main nodes are:

```text
agent
tools
```

And the edges are:

```text
START → agent
agent → tools or END
tools → agent
```

### Acceptance

Without looking at source code, draw the graph and explain why every edge exists.

---

## TODO 7: Implement conditional routing

Conceptually:

```python
def should_continue(state):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tools'
    return 'end'
```

Then wire conditional edges from `agent`.

### Deliberate failure

Temporarily remove:

```text
tools → agent
```

Observe what is missing after the Tool executes.

### Explain

The Tool result is often not the final user-facing answer. It becomes a `ToolMessage`, then the LLM reasons over that result to produce natural language.

---

## TODO 8: Inspect the full Tool Calling message sequence

Log or debug the graph state and identify:

```text
HumanMessage
AIMessage(tool_calls=[...])
ToolMessage(result=...)
AIMessage(final answer)
```

### Acceptance

You can explain:

> Tool execution and answer generation are separate steps. The application controls the tool, and the LLM usually turns the structured result into the final response.

---

## TODO 9: Understand feature-gated tools

In the current project, RAG is not always available.

Runtime configuration can disable it:

```env
ENABLE_RAG=false
```

The graph should only register/use the RAG Tool when the feature is enabled.

### Acceptance

You can explain why feature flags are safer than scattering “if provider exists” checks across unrelated business logic.

This becomes more important when an application supports:

```text
mock
text
full
```

modes with different external dependencies.

---

## TODO 10: Separate Agent reasoning from transport streaming

The Agent graph determines **what should happen**:

```text
LLM
 ↓
Tool?
 ↓
Tool execution
 ↓
LLM again
```

SSE determines **how partial output is transported to the browser**.

These are different concerns.

### Acceptance

You can explain why you should be able to debug:

```text
Agent/Tool logic
```

without first blaming:

```text
SSE framing
```

and vice versa.

---

## Reference mental model

LangGraph is not making the LLM “more intelligent.” It makes the **execution workflow explicit and controllable**.

```text
model reasons
  ↓
external action needed?
  ├─ no  → finish
  └─ yes → controlled Python Tool
                ↓
            ToolMessage
                ↓
            model reasons again
```

This explicit loop gives maintainers places to add:

- validation;
- permissions;
- feature flags;
- logging;
- cancellation;
- evaluation;
- security checks.

---

## Common errors

### Tool never triggers

Check:

- whether the tool description/docstring clearly explains when to use it;
- whether the tool is actually bound/registered;
- whether the user question requires the tool;
- whether feature flags disabled the tool.

### `last_message.tool_calls` is missing

Verify that the last state item is the expected AI message type and that your routing function handles message variants safely.

### Infinite tool loop

The model keeps requesting the tool, or the tool result/routing logic does not give it enough information to finish.

Inspect the full state sequence, not only the final UI.

### Conversation state becomes strange

Inspect message order and the `add_messages` reducer/state merge behavior.

### Tool result leaks unsafe data

Remember that Tools cross a trust boundary. A Tool should not casually expose secrets, absolute server paths, another user’s data, or unrestricted side effects.

---

## Challenge

Add a deterministic local Tool:

```python
@tool
def calculate_rectangle_area(width: float, height: float) -> float:
    return width * height
```

Requirements:

1. Normal small talk should not call it.
2. A rectangle-area question should call it.
3. The Tool returns a numeric result.
4. The LLM produces the final natural-language answer.
5. Add one test or reproducible trace proving the Tool was actually invoked.

Then write a short explanation:

> Why is deterministic calculation a better fit for a Tool than asking a language model to “estimate from language intuition”?

---

Previous: [Chapter 07 — SSE Streaming](./chapter-07-sse.md)  
Next: [Chapter 10 — RAG + LanceDB](./chapter-10-rag.md)
