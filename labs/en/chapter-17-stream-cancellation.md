# Chapter 17 Lab: Async Work, Streaming, Cancellation, and Resource Cleanup

🌐 **Language:** [中文](../chapter-17-stream-cancellation.md) | **English**

## Goal

Understand that a user clicking **Stop** is not merely a UI-state change. It is a cross-layer cancellation problem.

Current AiFriends implements a path like:

```text
InputField.vue AbortController
        ↓
streamApi signal
        ↓
browser terminates current SSE request
        ↓
Django StreamingHttpResponse generator closes
        ↓
generator finally → cancel_event.set()
        ↓
LLM/TTS worker observes cancellation and stops as early as possible
```

The exact amount of remote compute that can be cancelled still depends on the external provider.

---

## TODO 1: Compare stale-result suppression with real cancellation

A simple old-style technique is:

```text
processId++
ignore late chunks
stop local audio
```

That protects the UI from stale data, but it may leave the network/model work running.

Current behavior adds:

```js
AbortController.abort()
```

### Explain

> Why can “the UI stopped displaying output” still mean “the model is generating and consuming tokens in the background”?

Separate:

```text
presentation cancellation
network cancellation
local worker cancellation
remote provider cancellation
```

---

## TODO 2: Observe the Network request

Send a prompt that produces a long response, then click Stop during streaming.

DevTools → Network:

Record:

```text
request start time
Stop click time
request end/abort time
status shown by browser
remaining SSE events after Stop
```

### Acceptance

- the streaming request actually closes;
- old chunks do not continue updating the UI;
- a normal user abort is not surfaced as a scary business failure.

---

## TODO 3: Follow `AbortSignal` through the frontend

Trace:

```text
InputField.vue
  ↓ activeController
streamApi(..., signal)
  ↓
fetch-event-source / request client
```

Answer:

- where the controller is created;
- when the previous controller is aborted;
- what happens on component/chat close;
- why `processId` remains useful as defense-in-depth even with actual abort.

---

## TODO 4: Understand the backend Queue

The chat backend bridges:

```text
synchronous Django generator
async LangGraph / WebSocket work
```

A thread-safe Queue carries messages between them:

```text
async/background producer
        ↓ put()
      Queue
        ↓ get()
sync SSE generator
```

Draw and label:

```text
who puts text?
who puts audio?
who puts errors?
who gets events?
what does None/sentinel mean?
what does cancel_event mean?
```

### Important distinction

```text
sentinel     → producer is finished; consumer can stop waiting
cancel_event → cancellation requested; worker should stop producing
```

They solve related but different problems.

---

## TODO 5: Handle three failure classes

Simulate/consider:

```text
LLM connection fails
TTS connection fails
browser disconnects halfway through
```

Requirements:

- generator must not block forever on `mq.get()`;
- worker must send/trigger a completion path;
- frontend must not retry forever;
- normal `AbortError` must not be treated as a server crash;
- unexpected worker exceptions should reach logs and/or an SSE error event.

---

## TODO 6: Understand `finally` as a cleanup boundary

Streaming code often exits in more than one way:

```text
normal completion
user abort
route change
browser/network disconnect
exception
```

The generator's `finally` block is valuable because it runs cleanup even when the happy-path loop does not finish normally.

### Acceptance

You can explain why cancellation logic only placed after the normal streaming loop is insufficient.

---

## TODO 7: Decide what to persist after cancellation

Current normal completion persists a complete `Message`.

Design and compare:

```text
A. cancelled response is not persisted
B. persist partial AI output with partial=true
C. persist user message + AI status=cancelled
```

For each design answer:

- what fields change in the database?
- how does history UI render it?
- should token usage be stored if available?
- should partial AI text enter long-term memory?
- should a retry create a new row or update the old one?

There is no single correct answer; the important part is making cancellation semantics explicit.

---

## TODO 8: Add timeouts conceptually

Consider separate limits for:

```text
provider connection timeout
LLM generation timeout
TTS handshake timeout
overall chat deadline
```

### Explain the difference

```text
user cancel → explicit user/application intent
timeout     → time budget expired
failure     → operation cannot proceed because of an error
```

These should not necessarily share the same UI message, metrics, or retry policy.

---

## TODO 9: Resource cleanup on the browser

Stopping network traffic is not enough if media resources remain alive.

Depending on state, clean up:

```text
pause audio
clear audio queue
stop accepting old chunks
end MediaSource where safe
revoke object URLs
reset source buffer/player state
abort old network controller
```

### Acceptance

Switch between two Friends while the first one is generating speech. No old audio/chunks should leak into the second chat.

---

## TODO 10: Think about cancellation reasons

Useful reasons might include:

```text
user_stop
new_message
route_change
chat_closed
browser_disconnect
timeout
```

These reasons help observability because “cancelled” alone does not tell you whether users dislike long answers, the UI routinely restarts streams, or network connections are unstable.

---

## Acceptance

- [ ] Stop truly ends the browser SSE request.
- [ ] You can explain `AbortController` and `AbortSignal`.
- [ ] You can explain Queue + sentinel + `cancel_event`.
- [ ] Backend cleanup does not permanently block after cancellation.
- [ ] You can design a partial-message persistence policy.
- [ ] You distinguish cancel / timeout / failure.
- [ ] You can explain why remote provider cancellation may still be best-effort.

---

## Challenge

Propagate a cancellation reason into structured backend logs, for example:

```text
request_id
friend_id
cancelled=true
cancel_reason=user_stop
elapsed_ms
chunks_emitted
```

Then design a small report that answers:

```text
What percentage of chats are cancelled?
Which reason is most common?
How long do users wait before cancelling?
Does TTS increase cancellation?
```

The goal is to turn cancellation from an invisible control-flow edge case into an observable product behavior.
