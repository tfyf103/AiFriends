# Chapter 12 Lab: Streaming TTS — Let the Character Speak While Text Is Generated

🌐 **Language:** [中文](../chapter-12-tts.md) | **English**

## Goal

Upgrade this slow pipeline:

```text
LLM finishes full answer
  ↓
run TTS once
```

into a concurrent streaming pipeline:

```text
LLM text chunk
  ├→ SSE text → browser renders
  └→ TTS WebSocket → MP3 bytes → Base64 SSE → browser plays
```

The user should see text and hear speech progressively.

---

## Historical checkpoints

```text
845dcb620d0ce2f77f50b8c8dc94b91de338a58b  TTS backend
8615f6607406be373ae9ce7b09934d5a4da496c6  frontend audio playback
88343a97f0d74570e10bfe3952c0192669876a61  per-Character voice selection
```

Current AiFriends has since made TTS optional and configurable through:

```text
ENABLE_TTS
TTS_MODEL
WSS_URL
Character.voice
```

Real text chat no longer requires TTS to be healthy.

---

## TODO 1: Prove one-shot TTS first

Before concurrency, synthesize a fixed sentence:

```text
Hello, I am AiFriends.
```

Save/play the returned MP3.

### Acceptance

Prove independently that:

- provider credentials work;
- `WSS_URL` is correct;
- the configured TTS model is accepted;
- the selected `voice_id` is valid;
- MP3 bytes are actually returned.

Do not debug LLM streaming and TTS provider configuration at the same time.

---

## TODO 2: Understand why concurrency matters

Sequential example:

```text
LLM: 5 s
  ↓
TTS: 3 s
  ↓
first audio heard after ~8 s
```

Desired experience:

```text
first useful text chunk
  ↓ immediately feed TTS
  ↓
first audio can start before full LLM answer is complete
```

Measure perceived latency, not only total completion time.

---

## TODO 3: Respect the TTS feature flag

Current AiFriends supports:

```env
ENABLE_TTS=false
```

When disabled, chat should still use the real text/LLM path and stream text without connecting to the speech WebSocket.

If a Character has no usable Voice, the maintained chat path can also fall back to text-only behavior instead of crashing.

### Acceptance

- [ ] `text` mode works without TTS credentials.
- [ ] disabling TTS means no WSS connection.
- [ ] missing Voice does not make text chat unusable.
- [ ] `doctor` only requires speech configuration when the selected feature set needs it.

---

## TODO 4: Start the TTS WebSocket task

Send the provider's equivalent of:

```text
action: run-task
task_group: audio
task: tts
function: SpeechSynthesizer
```

with runtime-configured model/voice parameters such as:

```text
model: <TTS_MODEL>
voice: <Character voice_id>
format: mp3
sample_rate: ...
volume/rate/pitch: ...
```

Wait for the provider's task-start event before streaming text.

### Key lesson

Provider WebSocket protocols are not standardized just because the chat HTTP API is OpenAI-compatible.

---

## TODO 5: Stream LLM output with one producer and two destinations

Current LangGraph usage concept:

```python
async for msg, metadata in app.astream(
    inputs,
    stream_mode='messages',
):
    ...
```

For each content chunk:

1. enqueue a browser text event;
2. send appropriate text to the TTS task.

```text
LLM chunk
├→ Queue → SSE content
└→ TTS WebSocket
```

### Think about chunk boundaries

Should every tiny token/string be sent directly to TTS?

Compare:

```text
per token
per punctuation boundary
per sentence
fixed character window
```

Trade off first-audio latency against speech naturalness and provider overhead.

---

## TODO 6: Receive binary audio

When the TTS WebSocket yields binary MP3 data:

```python
bytes
```

current AiFriends turns it into Base64 text so it can travel inside JSON-shaped SSE events:

```python
audio = base64.b64encode(msg).decode('utf8')
```

then queues:

```python
{'audio': audio}
```

### Explain Base64

SSE events are text frames. Base64 is a practical bridge for binary payloads, but it increases size and is not the only possible production architecture.

---

## TODO 7: Understand Thread + asyncio + Queue

The backend bridges multiple execution models:

```text
Django synchronous streaming generator
        ↑
thread-safe Queue
        ↑
background Thread
        ↓
asyncio.run(...)
        ↓
LangGraph + WebSocket async tasks
```

You should be able to label:

```text
producer
consumer
cancellation signal
completion sentinel
error propagation
```

### Why a Queue?

It decouples asynchronous producers from the synchronous SSE consumer without requiring both sides to run in the same execution model.

---

## TODO 8: Completion and error signals

A worker must always give the consumer a way to stop waiting.

The learning architecture uses a sentinel pattern such as:

```python
mq.put_nowait(None)
```

The SSE generator exits when it receives the sentinel.

### Deliberate failure

On an experiment branch, remove the completion signal.

Observe how the generator can remain blocked on `mq.get()` even though the worker has already finished or failed.

Then restore reliable cleanup in `finally` paths.

---

## TODO 9: Decode Base64 in the browser

Concept:

```js
const binaryString = atob(base64Data)
const bytes = new Uint8Array(binaryString.length)
```

Copy each decoded byte into the array.

Do not pass the Base64 characters themselves to an MP3 decoder as if they were the original audio bytes.

---

## TODO 10: Stream audio with `MediaSource` and `SourceBuffer`

Create:

```js
mediaSource = new MediaSource()
audioPlayer.src = URL.createObjectURL(mediaSource)
```

then:

```js
sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg')
```

Incoming audio:

```text
MP3 bytes
  ↓
audioQueue.push(bytes)
  ↓
processQueue()
```

### Why queue audio on the frontend?

`SourceBuffer.appendBuffer()` cannot be called arbitrarily while the buffer is already `updating`.

Use `updateend` to append the next queued chunk.

---

## TODO 11: Stop old speech for real

Closing a chat, switching Friend, starting a new request, or clicking Stop should clean up both network and audio state.

Current frontend behavior combines:

```text
AbortController → terminate current SSE request
processId        → ignore stale callbacks defensively
stop audio       → pause / clear queues / release media resources
```

Backend cancellation uses the streaming generator's close/finally path to set a cancellation event for the worker.

### Acceptance

Character A is speaking. Close/switch to Character B.

A's old stream/audio must not continue writing into B's conversation UI or playback pipeline.

---

## TODO 12: Use per-Character Voice

Do not hard-code a provider voice string in the TTS worker.

Resolve:

```text
Friend
  ↓
Character
  ↓
Voice
  ↓
voice_id
```

and use the provider-specific `voice_id` only when TTS is enabled and a voice is available.

---

## Reference architecture

```text
              ┌→ text SSE → UI
LLM stream ───┤
              └→ TTS WebSocket
                      ↓
                  audio bytes
                      ↓
                  Base64 SSE
                      ↓
                 MediaSource
```

The difficult part is not the TTS API itself. It is **coordinating concurrent data streams, cancellation, completion, and browser playback state**.

---

## Common errors

### Text works, no sound

Check one boundary at a time:

1. TTS feature enabled?
2. valid Character Voice?
3. provider task started?
4. binary audio received?
5. SSE contains `audio` events?
6. browser decoded Base64?
7. `MediaSource` supports `audio/mpeg`?
8. autoplay policy blocked `play()`?

### `SourceBuffer is updating`

Your audio appends are not serialized through a queue/updateend loop.

### Audio stutters

Inspect chunk size, network/provider latency, queue starvation, and unnecessary MediaSource resets.

### Audio continues after Stop

The request may be aborted but local media state was not cleared, or a stale callback still has access to the old player state.

### TTS failure breaks all chat

That is the coupling Chapter 16/17 asks you to avoid. Text capability should survive optional speech failure when the configured mode allows it.

---

## Challenge: Measure perceived latency

Record:

```text
T0 = user clicks Send
T1 = first text chunk rendered
T2 = first audible audio begins
```

Calculate:

```text
TTFT-text  = T1 - T0
TTFA-audio = T2 - T0
```

Then propose at least three changes that specifically improve **time to first audio**, for example:

- sentence/chunk aggregation strategy;
- earlier TTS task handshake;
- provider/model choice;
- network locality;
- buffering thresholds;
- overlapping more of the LLM and TTS work.

Do not confuse reducing total completion time with improving perceived responsiveness.
