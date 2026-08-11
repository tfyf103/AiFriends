# Chapter 11 Lab: ASR — From Browser Microphone to Text

🌐 **Language:** [中文](../chapter-11-asr.md) | **English**

## Goal

Let the user speak instead of typing:

```text
Microphone
  ↓
browser audio
  ↓ convert to PCM 16 kHz
FormData(audio)
  ↓ HTTP
Django ASR endpoint
  ↓ WebSocket
ASR provider
  ↓ transcription
Django JSON
  ↓
Vue feeds text into the existing chat pipeline
```

The important architectural idea is that ASR is an **input adapter**. Once speech becomes text, the normal chat system should not care whether that text came from a keyboard or microphone.

---

## Historical checkpoints

```text
02cbc4f7567ebbed95eba483724611c35b6f6b1f  frontend voice input
5c0f6473fefad53542280257399d830663c8683a  backend speech recognition
```

Historical commits may contain provider/model names that differ from current `main`.

Current AiFriends uses runtime configuration through:

```text
backend/web/ai/config.py
ASR_MODEL
ENABLE_ASR
WSS_URL
```

Do not treat a historical hard-coded ASR model as a permanent requirement.

---

## TODO 1: Keep ASR and TTS directions straight

```text
ASR: Audio → Text
TTS: Text → Audio
```

This chapter is only about ASR.

If you mix the two directions while debugging, you will inspect the wrong subsystem.

---

## TODO 2: First prepare browser VAD/runtime assets

Before experimenting with voice features:

```bash
cd frontend
npm run setup:vad
```

The setup script copies the VAD and ONNX Runtime assets needed by the browser into the public directory.

Then verify your environment:

```bash
cd ../backend
python manage.py doctor
```

### Why this matters

Current AiFriends intentionally keeps speech optional. A learner should be able to run text/mock mode without having working VAD, ASR, or TTS credentials.

---

## TODO 3: Request microphone permission

Your UI should support at least:

```text
start recording
stop recording
cancel
```

### Acceptance

- [ ] the browser asks for microphone permission;
- [ ] denying permission does not crash the UI;
- [ ] recording/audio resources are cleaned up when the component closes;
- [ ] you can distinguish “permission denied” from “backend ASR failed.”

---

## TODO 4: Understand sample rate and PCM

The speech backend expects a concrete audio representation such as:

```text
sample_rate = 16000
format = pcm
```

You must know what the frontend is actually sending.

### Explain

Why is this wrong?

```text
record browser WebM/MP3
rename file to voice.pcm
assume it is PCM
```

A file extension does not change the underlying encoding.

---

## TODO 5: Upload audio as multipart form data

Frontend concept:

```js
const formData = new FormData()
formData.append('audio', blob, 'voice.pcm')
```

Endpoint:

```text
POST /api/friend/message/asr/asr/
```

Backend reads:

```python
audio = request.FILES.get('audio')
```

### Acceptance

Network shows `multipart/form-data`, and Django receives the file under the expected field name.

---

## TODO 6: Prove the HTTP/UI path before connecting a provider

Before a real ASR WebSocket, temporarily return:

```json
{
  "result": "success",
  "text": "ASR TEST"
}
```

Have Vue feed `ASR TEST` into the normal chat-send logic.

### What this proves

```text
recording component
  ↓
HTTP upload
  ↓
ASR response shape
  ↓
Vue chat input reuse
```

If this works but real ASR does not, the failure is outside the basic Vue/Django integration.

---

## TODO 7: Respect the ASR feature flag

Current AiFriends supports:

```env
ENABLE_ASR=false
```

When ASR is disabled, the endpoint should fail clearly (current behavior uses `503 Service Unavailable`) rather than trying to connect to a missing speech WebSocket.

### Acceptance

- [ ] `mock`/text learning works with ASR disabled;
- [ ] enabling ASR changes the required environment checks;
- [ ] `doctor` explains missing speech configuration;
- [ ] no real WSS call occurs when the feature is disabled.

---

## TODO 8: Start the provider WebSocket task

The backend gets provider configuration through environment/settings, conceptually:

```text
API_KEY
WSS_URL
ASR_MODEL
```

Establish the WebSocket and send the provider's task-start payload.

The exact event names and payload fields are provider-specific. Your current model should come from configuration rather than being hard-coded in the View.

### Acceptance

Wait for the provider's equivalent of:

```text
task-started
```

before streaming PCM bytes.

---

## TODO 9: Send PCM in chunks

A learning implementation may send chunks such as:

```python
chunk_size = 3200
```

then:

```python
await ws.send(pcm_data[i:i + chunk_size])
await asyncio.sleep(...)
```

### Explain why streaming protocols use chunks

- incremental processing;
- backpressure/network pacing;
- lower latency;
- provider protocol requirements;
- avoiding one huge in-memory/network frame.

---

## TODO 10: Send and receive concurrently

Do not model a duplex WebSocket as:

```text
send entire audio
then start reading responses
```

Use concurrent sender/receiver tasks, for example:

```python
await asyncio.gather(
    asr_sender(...),
    asr_receiver(...),
)
```

### Acceptance

You can explain what “full duplex” means in this ASR context.

---

## TODO 11: Handle partial vs final transcription

Providers often send intermediate hypotheses and final sentence results.

Only append final/sentence-end results to the final text unless your UI explicitly wants live partial text.

### Deliberate failure

Append every partial result and every final result into one string.

Observe duplicated/repeated transcription, then fix the state model.

---

## TODO 12: Reuse the existing chat pipeline

When ASR returns:

```json
{
  "text": "What time is it?"
}
```

do **not** build another LLM pipeline.

Reuse the same send logic:

```text
keyboard text ─┐
               ├→ normalized text → same Chat pipeline
ASR text ──────┘
```

This keeps authentication, SSE, persistence, memory, RAG, and cancellation behavior shared.

---

## Reference mental model

```text
Input adapters
├── keyboard
└── microphone
      ↓
     ASR
      ↓
normalized text
      ↓
existing chat system
```

ASR should not become a second copy of the chat application.

---

## Common errors

### Browser records silence

Check permission, selected input device, and recording state before touching Django.

### ASR output is nonsense

Inspect the actual audio encoding, channel count, sample rate, and PCM conversion.

### WebSocket authentication fails

Check provider `API_KEY`, headers, account/model permissions, and `WSS_URL`.

### Task never starts

Log provider text/control events and compare the task payload to that provider's protocol.

### The same sentence appears multiple times

You probably append both partial and final transcription events.

### ASR returns 503

Check:

```env
ENABLE_ASR=true
```

then run:

```bash
python manage.py doctor
```

---

## Challenge

Add a voice activity indicator:

```text
silence
speaking
sentence ended
```

Then explain the distinction:

```text
VAD → is someone speaking?
ASR → what did they say?
```

Finally measure:

```text
recording end → ASR final text latency
```

and identify whether delay comes from browser conversion, upload, WebSocket handshake, provider processing, or response parsing.
