# Chapter 07 Lab: SSE Streaming Chat and Message Persistence

🌐 **Language:** [简体中文](../chapter-07-sse.md) | **English**

## Goal

Upgrade the previous chapter from:

```text
wait for complete answer → one JSON response
```

to:

```text
model produces a chunk
  ↓
Django emits immediately
  ↓
browser displays immediately
```

Then persist the completed conversation and token metadata to `Message`.

The current project also supports real request cancellation and a shared access-token refresh path for Axios and SSE. This lab teaches both the basic protocol and the current engineering behavior.

---

## Historical checkpoints

Useful Git-history checkpoints:

```text
b9ea1c3404b04413d638067de78c3ed4d7262fc3  backend streaming output
3c7c464b51dcbb411ad50bafe58ad214ecc6eb2c  frontend streaming reply
ea419695f4d8e9e2cec97c4f92a03dc7d679e4df  streaming history loading
```

Compare the transition from one-shot chat to streaming:

```bash
git diff 72a9866e3370481a8fa6e070e55c7784977c058a b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

Historical code may contain bugs fixed later; use it to study evolution, not as the final reference implementation.

---

## TODO 1: Write a fake SSE stream first

Do not call an LLM yet.

Create a generator conceptually like:

```python
def event_stream():
    yield 'data: {"content":"Hel"}\n\n'
    yield 'data: {"content":"lo"}\n\n'
    yield 'data: [DONE]\n\n'
```

Return it with:

```python
StreamingHttpResponse(
    event_stream(),
    content_type='text/event-stream',
)
```

### Acceptance

The browser receives separate events before the HTTP request closes:

```text
Hel
lo
[DONE]
```

Prove the transport first, then insert the model.

---

## TODO 2: Understand SSE framing

An event is separated by a blank line:

```text
data: ...\n\n
```

Why two newline characters?

Because the empty line terminates one SSE event frame.

### Deliberate failure

Change `\n\n` to `\n` in your experiment.

Observe whether the client delays dispatching the event.

Restore the correct framing afterward.

---

## TODO 3: Replace one-shot generation with streaming

The current LangGraph path can stream messages/chunks rather than waiting for one final answer.

Conceptually:

```python
async for msg, metadata in app.astream(
    inputs,
    stream_mode='messages',
):
    ...
```

or an equivalent streaming API for your experiment.

For each content-bearing chunk, emit an SSE payload:

```python
yield f'data: {json.dumps({"content": msg.content})}\n\n'
```

### Acceptance

In DevTools → Network:

- [ ] one HTTP request stays open;
- [ ] the UI receives useful content before the request finishes;
- [ ] the final content is the concatenation of the chunks, not just the last chunk.

---

## TODO 4: Understand the frontend SSE client

AiFriends uses `fetch-event-source` rather than waiting for a normal Axios JSON response.

Understand these lifecycle hooks/concepts:

```text
onopen
onmessage
onerror
onclose
AbortSignal
```

Special case:

```text
[DONE]
```

Do not blindly run:

```js
JSON.parse('[DONE]')
```

### Acceptance

For each event such as:

```json
{"content": "chunk"}
```

append the content to the current AI message.

---

## TODO 5: Implement optimistic chat UI

Immediately after send:

```text
append user message
append empty AI message
```

Then incoming chunks update only the last AI message:

```text
''
'H'
'He'
'Hello'
'Hello, I...'
```

### Explain

Why not create one new bubble for every token/chunk?

Because the chunks are transport fragments of one logical assistant message.

---

## TODO 6: Persist the complete Message

During streaming, maintain accumulated output and token/usage information.

Conceptually:

```python
final_output = ''
final_usage = {}
```

For every text chunk:

```python
final_output += msg.content
```

When the generation path completes normally, persist the logical message record.

At minimum, understand these fields:

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
```

### Acceptance

The database `output` contains the whole assistant answer, not only the final chunk.

### Engineering note

Streaming introduces lifecycle questions such as when to emit `[DONE]`, when to persist partial output, and what to do on cancellation. These are product/data-consistency decisions, not just protocol details.

---

## TODO 7: Load older chat history incrementally

The history endpoint uses a cursor-like message ID pattern:

```text
GET /api/friend/message/get_history/
```

Parameters include:

```text
friend_id
last_message_id
```

Conceptually:

```text
last_message_id = 0 → latest page
last_message_id > 0 → older rows where id < last_message_id
```

### Frontend challenge

When older messages are inserted above the current viewport, the user should not suddenly jump to the top.

Track values such as:

```text
scrollHeight before insert
scrollHeight after insert
scrollTop
```

and compensate for the height delta.

---

## TODO 8: Handle an expired JWT in SSE

Normal Axios requests have their own interceptor path, while SSE is a different transport wrapper.

The current project intentionally shares one refresh operation between them.

Target behavior:

```text
SSE starts
  ↓
server returns 401
  ↓
refreshAccessToken()
  ↓
single-flight refresh
  ↓
Pinia gets the new access token
  ↓
rebuild Authorization header
  ↓
reconnect SSE request
```

### Important lesson

A failed/closed stream cannot magically resume in place. The client must establish a new request with valid credentials.

### Concurrency experiment

Trigger multiple expired requests around the same time and inspect whether the client creates one refresh request or a refresh storm.

The desired behavior is a shared in-flight refresh Promise.

---

## TODO 9: Implement real Stop Generation

A mature streaming UI needs cancellation, not only stale-response filtering.

Browser side:

```text
new request
  ↓
AbortController
  ↓
streamApi(..., signal)
```

On Stop:

```text
controller.abort()
  ↓
network request closes
  ↓
spinner/stream state ends
  ↓
audio playback stops if active
```

The project also keeps a process/stale-response ID as an extra guard so callbacks from an obsolete chat cannot mutate the new conversation.

### Acceptance

In DevTools → Network, clicking Stop should actually close/cancel the active request rather than merely hiding new text.

---

## TODO 10: Understand backend disconnect propagation

The backend owns a cancellation event used by the generation worker.

Conceptual flow:

```text
client aborts / disconnects
      ↓
streaming generator closes
      ↓
generator finally block
      ↓
cancel_event.set()
      ↓
worker checks cancellation
      ↓
stops work as soon as practical
```

### Explain

Why is backend cancellation still useful if the browser already stopped rendering?

Because otherwise the server/provider may continue consuming CPU, model tokens, or TTS work for a response nobody will receive.

---

## Reference mental model

Backend:

```text
model / graph stream
    ↓
accumulate logical output
    ↓
yield SSE frames
    ↓
StreamingHttpResponse
```

Frontend:

```text
fetchEventSource
    ↓ onmessage
parse event
    ↓
update reactive history
    ↓
Vue re-renders one AI bubble
```

Cancellation:

```text
AbortController
    ↓
network disconnect
    ↓
backend cancel_event
```

---

## Common errors

### Backend yields chunks but browser shows everything at the end

Check:

- `Content-Type: text/event-stream`;
- SSE framing ends with a blank line;
- proxy/server buffering behavior;
- `X-Accel-Buffering` if relevant in a proxy deployment.

### `[DONE]` causes a JSON parse error

Handle the sentinel before parsing JSON.

### Old reply appears in a new Friend chat

Inspect AbortController cancellation and stale process-ID protection.

### Stored output is empty

You emitted chunks but forgot to accumulate the final logical response.

### Refresh succeeds but the reconnect still uses the old token

Verify that the refresh result updates the central auth store and that the SSE Authorization header is rebuilt **after** refresh.

### Stop button changes UI but request remains open

You implemented visual suppression, not network cancellation.

---

## Challenge

Model the frontend stream as explicit states:

```text
idle
connecting
streaming
stopping
error
```

For each state, define:

- what the UI displays;
- whether Send is enabled;
- whether Stop is enabled;
- whether an AbortController should exist;
- what should happen to partial output.

This moves the implementation from “streaming works” toward a real product state machine.

---

Previous: [Chapter 06 — Minimal LLM Chat](./chapter-06-basic-chat.md)  
Next: [Chapter 08 — LangGraph Tool Calling](./chapter-08-langgraph-tools.md)
