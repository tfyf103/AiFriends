# Chapter 20 Lab: CI, Build, Deployment, and Observability

🌐 **Language:** [中文](../chapter-20-ci-deploy-observability.md) | **English**

## Goal

Upgrade from:

> “It works on my laptop.”

into:

> **“Every change is checked automatically, builds are reproducible, and failures can be traced in a running system.”**

---

## TODO 1: Read the GitHub Actions workflow

Open:

```text
.github/workflows/ci.yml
```

The maintained workflow currently checks the repository through backend, frontend, and learning-image jobs, including:

```text
Python compile
Chapter 00–20 structural grader
Django migration drift check
Django system check
Django behavior tests
npm ci
VAD/ONNX asset setup
frontend quality check
Node tests
Vite production build
Docker learning image build
```

### Explain Mock mode in CI

Why does CI use a deterministic local AI mode instead of spending real LLM/TTS credits for every PR?

Your answer should include:

- reproducibility;
- contributor security/secrets;
- provider outages/rate limits;
- cost;
- fast feedback;
- what Mock mode still does **not** validate.

---

## TODO 2: Deliberately make CI fail

On a learning branch, choose one:

```text
break the singleFlight unit test
add trailing whitespace caught by quality check
introduce a Python syntax error
create migration drift
remove a required import
break the frontend build
```

Push/open a PR and watch the failing job.

Fix the root cause and verify the next run becomes green.

### Lesson

CI is not a badge decoration. It is a machine-enforced merge gate/feedback system.

---

## TODO 3: Understand Dev Server vs Build

Development:

```bash
npm run dev
```

Production-style frontend asset build:

```bash
npm run build
```

Current Vite configuration generates a manifest.

Django reads the manifest instead of hard-coding filenames such as:

```text
index-abc123.js
index-def456.css
```

### Explain content hashes

Hashed asset names may change when content changes. A server-side template that hard-codes yesterday's hash can break after the next build.

The manifest is the mapping between logical entry and generated artifact names.

---

## TODO 4: Inspect the Health endpoint

Endpoint:

```text
GET /api/health/
```

It is public and intentionally minimal.

Current health data includes concepts such as:

```text
status
database
ai_mode
feature states
request_id
```

Database failure can degrade health and return a service-unavailable status.

### Never expose

```text
API keys
DB passwords
full stack traces
private conversations
provider secrets
```

A health endpoint should be operationally useful without becoming an information leak.

---

## TODO 5: Follow `X-Request-ID`

AiFriends middleware:

```text
backend/web/middleware.py
```

preserves an incoming request ID or generates one, then returns it in:

```http
X-Request-ID: ...
```

### Exercise

Send:

```http
X-Request-ID: lab-123
```

and verify the response preserves it.

Then design log records so the same ID can connect:

```text
HTTP request
chat worker
RAG retrieval
TTS provider call
error event
```

---

## TODO 6: Design structured chat logs

A useful record might contain:

```text
request_id
user_id (or privacy-safe internal identifier)
friend_id
ai_mode
model
rag_used
tts_used
cancelled
cancel_reason
input_tokens
output_tokens
latency_ms
error_type
```

Do not blindly log full prompts/messages just because they are useful for debugging.

Balance observability with privacy.

---

## TODO 7: Choose meaningful metrics

Start with a small set:

```text
request count
4xx / 5xx rate
LLM latency
TTFT (time to first text token)
TTFA (time to first audio)
cancellation rate
tokens per request
RAG tool-call rate
retrieval latency
memory update failure rate
ASR/TTS provider failure rate
```

### Key lesson

Observability begins with choosing questions worth answering, not installing the largest monitoring platform.

---

## TODO 8: Build the learning Docker image

Current repository includes:

```text
Dockerfile.learning
compose.learning.yml
```

Build:

```bash
docker build -f Dockerfile.learning -t aifriends:learning .
```

or:

```bash
docker compose -f compose.learning.yml up --build
```

The image demonstrates a reproducible multi-stage idea:

```text
Node stage
  ↓ npm ci / VAD setup / Vite build
Python stage
  ↓ install requirements / copy backend + built assets
```

### Boundary

This image intentionally remains a **learning** deployment artifact. It is not a production architecture guarantee.

---

## TODO 9: Explain why `runserver` is not a production server

Discuss:

```text
WSGI/ASGI production server
reverse proxy / TLS termination
static files
persistent media
PostgreSQL
process supervision
rate limits
secret management
backup/restore
metrics/tracing
```

Do not “productionize” by only changing `DEBUG=false`.

---

## TODO 10: Create a deployment checklist

At minimum consider:

```text
DEBUG=false
SECRET_KEY from secure environment/secret manager
ALLOWED_HOSTS
HTTPS
secure cookies
CORS / CSRF policy
migrations applied
frontend assets built
persistent media/object storage
production database
backups
rate limits
health checks
structured logs
metrics / alerts
secret rotation
```

For every checklist item, state **who/what verifies it**.

---

## TODO 11: Add a bundle-size budget concept

A successful Vite build can still produce an unnecessarily large initial JavaScript bundle.

Design a CI budget such as:

```text
main entry must stay below X kB gzip
speech/VAD code should be lazy-loaded
route chunks should stay below thresholds
```

This connects build engineering to real user performance.

---

## TODO 12: Think about browser E2E

Current automated tests cover important backend/frontend units and behaviors, but a future browser E2E can verify the whole Mock journey:

```text
register
login
create Character
create Friend
send SSE message
Stop generation
reload/history
logout
```

Explain what this browser test would catch that unit tests may miss.

---

## Acceptance

- [ ] PRs automatically run CI.
- [ ] You intentionally caused and fixed one CI failure.
- [ ] You can explain Vite manifest-based asset loading.
- [ ] You can use `/api/health/` without exposing secrets.
- [ ] You understand `X-Request-ID` correlation.
- [ ] You chose meaningful latency/token/error metrics.
- [ ] You can build the learning Docker image.
- [ ] You can explain why the learning image is not the final production design.
- [ ] You can describe the difference between Build, Deploy, and Runtime Observability.

---

## Final engineering capstone

Choose one feature from the full course, for example:

```text
RAG citations
structured Memory
per-Character knowledge base
Stop/cancellation semantics
upload hardening
provider adapter
```

Deliver it as if maintaining a real open-source project:

```text
problem statement
architecture diagram
implementation
database migration if needed
API documentation
security analysis
automated tests
CI green
performance/latency considerations
observability plan
troubleshooting notes
```

If you can do this without relying on “it worked once on my machine,” you have moved from tutorial reproduction into software engineering practice.
