# Chapter 09 Lab: Long-Term Memory with `Friend.memory`

🌐 **Language:** [中文](../chapter-09-memory.md) | **English**

## Goal

Solve a real scaling problem:

```text
more and more chat turns
  ↓
if every historical message stays in every prompt forever
  ↓
context becomes longer, slower, and more expensive
```

AiFriends separates two forms of conversational state:

```text
short-term context → recent Message rows
long-term memory   → compressed summary in Friend.memory
```

---

## Historical checkpoint

```text
15a8a8427db9801f1fcc01da5d15cfdb97014111  long-term memory introduced
```

The maintained project later moved to a simple “every 5 stored Message rows” update trigger.

---

## TODO 1: Measure the cost of no long-term memory

Create around 20 turns of conversation.

Temporarily inspect the number and serialized size of messages sent to the model for:

```text
turn 1
turn 5
turn 10
turn 20
```

### Explain

If the full history grows forever, what happens to:

- input tokens;
- latency;
- cost;
- context-window pressure;
- the model's ability to focus on relevant information?

---

## TODO 2: Understand why memory belongs to `Friend`

Compare:

```text
User A ↔ Alice Character → memory A
User B ↔ Alice Character → memory B
```

`Character.profile` describes the shared AI identity.

`Friend.memory` describes user-specific relationship state.

### Acceptance

You can explain why putting memory directly on `Character` would leak/share one user's personal context into another user's relationship.

---

## TODO 3: Create a Memory SystemPrompt

In Django Admin, create a prompt with:

```text
title='记忆'
```

The exact language can vary, but the instruction should constrain the memory updater to:

- keep stable facts and useful preferences;
- remove low-value small talk;
- avoid inventing facts;
- let explicit new facts supersede outdated ones;
- keep output size controlled.

### Think

Long-term memory is not just “summarize this conversation.” A hallucinated memory can persist and influence many future turns.

---

## TODO 4: Build the MemoryGraph input explicitly

System message:

```python
SystemMessage(memory_prompt)
```

Human content concept:

```text
[Old Memory]
{friend.memory}

[Recent Conversation]
user: ...
ai: ...
```

### Acceptance

Inspect the final inputs. They should be explicit text/message structures, not raw Django model objects.

---

## TODO 5: Keep MemoryGraph intentionally small

The memory workflow can be:

```text
START → agent → END
```

Why no `ToolNode`?

Because the current task is a deterministic orchestration problem:

> Given old memory and recent conversation, ask the model for a revised compressed memory.

LangGraph is useful even when the graph is simple because it makes the workflow explicit.

---

## TODO 6: Persist the updated memory

Conceptually:

```python
friend.memory = res['messages'][-1].content
friend.update_time = now()
friend.save()
```

### Acceptance

Watch `Friend.memory` in Admin over time.

It should evolve with important facts without growing linearly with every chat token.

---

## TODO 7: Compare update frequencies

First, imagine/update memory on every message.

Record:

```text
extra model calls
latency
input/output tokens
```

Then use a simple trigger such as:

```python
if Message.objects.filter(friend=friend).count() % 5 == 0:
    update_memory(friend)
```

### Discuss alternatives

```text
every N turns
after token threshold
background job
only when a new stable fact is detected
user-triggered memory save
```

The current strategy is a learning-friendly policy, not an optimal universal memory architecture.

---

## TODO 8: Feed memory back into normal chat

The chat system prompt should include the current long-term memory, conceptually:

```text
[Long-term Memory]
{friend.memory}
```

Experiment:

1. Tell the Character: “My favorite color is green.”
2. Continue long enough to trigger memory update.
3. Later ask: “What is my favorite color?”

### Acceptance

The Character can use long-term memory without keeping the original old message permanently inside the short-term context window.

---

## TODO 9: Memory pollution experiment

Use an intentionally weak memory instruction such as:

```text
Freely summarize and add any useful information you think belongs here.
```

Observe whether the model invents stable facts that the user never said.

Then tighten the prompt.

### Key lesson

> A bad long-term memory is worse than a bad one-off answer because the error is persisted and repeatedly reintroduced into future prompts.

---

## TODO 10: Think about cancellation and memory timing

Current chat persistence/memory behavior is primarily designed around normally completed responses.

If a generation is cancelled halfway through, decide:

```text
Should the partial AI answer enter long-term memory?
Should only the user's completed statement count?
Should the memory update wait for a stable persisted Message?
```

This connects Chapter 09 to Chapter 17's cancellation semantics.

---

## Reference model

Memory update is a stateful compression function:

```text
new_memory = f(old_memory, recent_messages)
```

A useful memory tries to preserve:

```text
stable facts
preferences
important relationships
important events
goals / unfinished tasks
```

while dropping:

```text
repeated greetings
transient filler
verbatim history that has no long-term value
```

---

## Common errors

### `Friend.memory` stays empty

Check:

- whether the trigger threshold was reached;
- whether `update_memory()` actually ran;
- whether the `SystemPrompt(title='记忆')` exists;
- whether the configured memory model can be called.

### Memory updates but chat does not use it

You persisted memory but forgot to add it back into the normal chat system context.

### Every response becomes slower

You may be running an additional memory LLM call synchronously in the user-facing request path.

### The Character remembers incorrect facts

Inspect:

```text
memory prompt
old memory
recent conversation ordering
model output
```

Do not immediately blame the database.

---

## Challenge: Design structured memory

Design a schema such as:

```json
{
  "profile": [],
  "preferences": [],
  "relationships": [],
  "important_events": [],
  "open_tasks": []
}
```

For each memory item, consider adding:

```text
value
source_message_id
timestamp
confidence
status
```

Write down:

1. advantages over one free-text summary;
2. new complexity and migration cost;
3. how to update one field without corrupting unrelated fields;
4. how to represent conflicts and superseded facts;
5. what should never be stored for privacy reasons.

Chapter 19 turns this design into an evaluation problem.
