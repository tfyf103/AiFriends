# Chapter 13 Lab: Capstone — Trace and Modify One AiFriends Message End to End

🌐 **Language:** [简体中文](../chapter-13-capstone.md) | **English**

## Goal

This chapter does not introduce another framework API.

You must prove that you can reason about AiFriends as one system:

```text
Input
 ↓
Vue
 ↓
JWT / HTTP / SSE
 ↓
Django
 ↓
ORM / ownership
 ↓
LangChain / LangGraph
 ↓
Tool / RAG
 ↓
LLM
 ↓
optional TTS
 ↓
SSE
 ↓
MediaSource / UI
 ↓
Message persistence
 ↓
Long-term Memory
```

Final requirement:

> **Implement one small cross-layer change and explain exactly which layers it affects and why.**

Use the [English Architecture Guide](../../docs/ARCHITECTURE_EN.md) only after your first attempt to draw the flow yourself.

---

# Part A: Draw the whole request path from memory

Without reading docs, write down what happens after:

> “The user types a message in `InputField.vue` and presses Enter.”

Your diagram should include most of these concepts/files:

```text
InputField.vue
AbortController
streamApi.js
Authorization header
web/urls.py
MessageChatView.post()
Friend ownership
add_system_prompt()
add_recent_messages()
AI_MODE
CharGraph.create_app() for real model modes
agent
ToolNode when needed
LLM stream
optional TTS sender/receiver
Queue
event_stream()
SSE
InputField onmessage
MediaSource/audio path
Message persistence
update_memory()
```

### Acceptance

Only after drawing it yourself, compare with:

- [ARCHITECTURE_EN.md](../../docs/ARCHITECTURE_EN.md)
- `backend/web/views/friend/message/chat/chat.py`
- `backend/web/views/friend/message/chat/graph.py`
- `frontend/src/components/character/chat_field/input_field/InputField.vue`
- `frontend/src/js/http/streamApi.js`

Add missing nodes in a different color or annotation.

The purpose is not memorization; it is finding the gaps in your own systems model.

---

# Part B: Collect evidence from one real request

Open:

```text
Browser DevTools → Network
Django terminal/logs
```

Use either:

```text
AI_MODE=mock
```

for transport/auth/persistence evidence, or a real `text/full` mode when you specifically need Agent/Tool evidence.

Send a message such as:

```text
What is the exact current time?
```

Record actual evidence:

```text
1. Request URL:
2. HTTP method:
3. Authorization header shape:
4. Request body:
5. Response Content-Type:
6. First SSE data event:
7. Did the real Agent trigger get_time? (if using text/full)
8. Final [DONE] event:
9. Resulting Message.id:
10. input/output token data when available:
11. X-Request-ID:
12. What happens in Network when Stop is pressed?
```

### Acceptance

Every field must come from a real trace, database record, or log. Do not answer from memory.

---

# Part C: Prove that persona, memory, and RAG are different

Prepare three controlled experiments.

## 1. Character Profile

Set the character persona to something unique, for example:

```text
You are an engineer living in a lunar research station.
```

Ask:

```text
Where do you live?
```

Identify where the information enters the prompt:

```text
Character.profile
```

## 2. Long-term Memory

Tell the AI something user-specific:

```text
My favorite coffee is an unsweetened iced Americano.
```

After the memory update path has actually run, ask later:

```text
What kind of coffee do I usually like?
```

Identify:

```text
Friend.memory
```

## 3. RAG

Place one fact in your local knowledge base that is not in the character profile or conversation memory.

Ask a question that requires it.

Identify:

```text
LanceDB retrieval
   ↓
RAG Tool result
   ↓
Agent context
```

### Acceptance

You can explain why these should not be collapsed into one field:

```text
Character.profile = stable role/persona definition
Friend.memory     = user-specific compressed relationship memory
RAG evidence      = externally retrieved knowledge for a query
```

They have different lifecycles, ownership, update strategies, and trust/evaluation requirements.

---

# Part D: Failure-localization exam

For every symptom below, choose the **first layer** you would inspect and explain why.

## Failure 1

Clicking Send produces no Network request.

First inspection:

```text
Vue event / form handler / handleSend
```

Do not start in Django.

## Failure 2

Network shows HTTP 401.

First inspection:

```text
access token / refresh flow / Authorization header
```

Do not start with the LLM provider.

## Failure 3

SSE response contains `content`, but the chat bubble stays empty.

First inspection:

```text
streamApi onmessage
   ↓
callback/emit
   ↓
reactive history update
```

## Failure 4

Normal chat works, but a knowledge-base answer is wrong.

First inspection:

```text
retrieval result
```

Print the Documents before blaming generation.

## Failure 5

Text works, audio does not.

First inspection:

```text
TTS WebSocket / audio bytes / SSE audio event
```

Then trace toward the browser playback path.

## Failure 6

The AI forgot an old user preference.

First inspection:

```text
Was Friend.memory actually updated?
Was Friend.memory added to the SystemMessage?
```

## Failure 7

Clicking Stop hides new text, but the request continues in Network.

First inspection:

```text
AbortController / AbortSignal integration
```

## Failure 8

Several expired requests cause multiple refresh-token calls at once.

First inspection:

```text
single-flight refresh implementation
```

## Failure 9

Django returns an error but you cannot correlate it with a browser request.

First inspection:

```text
X-Request-ID
```

### Acceptance

For each failure, explain why the next layer should wait until the first layer is ruled out.

---

# Part E: Capstone modification — choose one

Implement one real change.

## Option A: Character Greeting

Add a field such as:

```text
greeting
```

Goal:

> Show a custom character greeting when a user opens a new conversation.

You must consider:

```text
Model
Migration
Create API
Update API
Get API
Serializer/validation where appropriate
Vue create form
Vue update form
Chat UI
Tests
```

### Bonus

Only show the greeting for a Friend with no persisted Messages, so an existing conversation does not receive the greeting again.

### Required engineering explanation

Why does this need a database migration rather than only a Vue state variable?

---

## Option B: First-class RAG citations

The current retrieval layer already keeps safe source information. Extend the product path so citations become explicit structured data rather than only text inside the Agent context.

Conceptual event:

```json
{
  "citation": {
    "source": "data.txt",
    "chunk": 3
  }
}
```

Consider:

```text
Document metadata
retrieval result schema
Tool return structure
chat/SSE event schema
frontend rendering
security: no absolute paths
RAG evaluation
regression tests
```

### Required engineering explanation

Why should source labels come from retrieval metadata instead of letting the LLM invent them?

---

## Option C: Improve Stop Generation semantics

The project already aborts the browser SSE request and propagates backend cancellation.

Choose one deeper product/data decision and implement it consistently:

```text
Should partial assistant output be persisted after cancellation?
Should it be marked as interrupted?
Should token usage be saved when available?
What happens to TTS audio already queued?
What happens if cancellation occurs during Tool/RAG execution?
```

Your implementation must consider:

```text
AbortController
streamApi signal
process/stale response ID
Django streaming generator
cancel_event
worker cleanup
MediaSource/audio cleanup
Message persistence policy
tests
```

### Required engineering explanation

“Stop rendering” and “stop work” are different. Explain which guarantees your change provides.

---

# Part F: Defense questions

After implementing the capstone, answer without looking at source code:

1. Which Vue states are involved in chat?
2. Why do normal JSON APIs and SSE use different transport wrappers?
3. Where are access and refresh credentials kept?
4. Why do Axios and SSE share one refresh operation?
5. How does Django verify that a `friend_id` belongs to the authenticated user?
6. What database constraint protects one Friend per user/character pair?
7. What does `bind_tools()` do?
8. What does `ToolNode` do?
9. Why is the `tools → agent` edge needed?
10. What is the difference between recent Message history and `Friend.memory`?
11. Where does RAG retrieval happen?
12. Why is retrieval evaluated separately from generation?
13. Are embeddings and generative chat models the same thing?
14. What directions do ASR and TTS convert?
15. Why is audio Base64-encoded in SSE?
16. What problem does `Queue` solve in the TTS architecture?
17. Why is AbortController better than only ignoring stale callbacks?
18. What does backend `cancel_event` add?
19. Why keep an `X-Request-ID`?
20. Which automated checks protect your capstone change?
21. What production concerns are deliberately outside `Dockerfile.learning`?
22. Which layers did your change affect, and why?

If you can answer these in your own words, you are no longer merely copying AiFriends; you understand the engineering model behind it.

---

# Final acceptance checklist

- [ ] I can start frontend and backend from a clean setup.
- [ ] I can run Mock mode without external AI credentials.
- [ ] I can use DevTools to localize request failures.
- [ ] I can explain JWT access/refresh behavior.
- [ ] I can explain SSE framing and the `[DONE]` sentinel.
- [ ] I can prove Stop closes the active browser request.
- [ ] I can explain LangChain message roles.
- [ ] I can draw the LangGraph Agent loop.
- [ ] I can implement a deterministic Tool.
- [ ] I can inspect RAG retrieval before generation.
- [ ] I can explain safe RAG source metadata.
- [ ] I can explain the `Friend.memory` update path.
- [ ] I can distinguish Character profile, memory, and RAG.
- [ ] I can distinguish ASR and TTS.
- [ ] I can explain the Queue/async/thread bridge.
- [ ] I can use tests/grader/build as evidence.
- [ ] I completed one cross-layer modification.
- [ ] I created my own Git commit for the capstone.

Suggested final learning commit:

```bash
git add .
git commit -m "learn: complete AiFriends full-stack capstone"
```

Then review your own history:

```bash
git log --oneline
```

---

Previous: [Chapter 10 — RAG + LanceDB](./chapter-10-rag.md)  
Continue: [English Architecture Guide](../../docs/ARCHITECTURE_EN.md)
