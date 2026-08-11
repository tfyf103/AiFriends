# AiFriends Engineering Course: Chapters 14–20

🌐 **Language:** [简体中文](./ENGINEERING_COURSE.md) | **English**

> Chapters 00–13 ask: **Can I build a complete full-stack AI application from scratch?**
>
> Chapters 14–20 ask: **Can I turn a working AI demo into software that is testable, maintainable, safer, deployable, and observable?**

---

## Course map

| Chapter | Topic | Real anchors in AiFriends |
|---|---|---|
| 14 | Testing / TDD | `backend/web/tests.py`, `frontend/tests/`, `scripts/grade.py`, GitHub Actions |
| 15 | DRF Engineering | Serializers, validation, HTTP status codes, error contracts |
| 16 | Config / Providers | `backend/web/ai/config.py`, `.env.example`, feature flags |
| 17 | Async / Streaming / Cancellation | `AbortController`, SSE, Queue, `cancel_event`, WebSocket |
| 18 | Data / Security | Friend uniqueness, safe migrations, ownership, uploads, privacy, prompt injection |
| 19 | RAG / Memory Evaluation | `retrieval.py`, eval cases, citations, structured memory, provenance/conflicts |
| 20 | CI / Build / Deploy / Observability | GitHub Actions, Vite manifest, health, request IDs, Docker, metrics |

English labs: [English Labs](../labs/en/README.md).

---

## Why a second stage exists

Many AI tutorials stop when the demo can:

```text
register
chat
use RAG
speak
```

Real maintenance questions begin after that:

```text
Who proves a change did not break login?
Why should concurrent 401s share one refresh?
If speech is down, why should text chat still work?
Does Stop actually terminate the stream/work?
Where did a RAG claim come from?
How do old and new memory facts conflict?
Why do built asset hashes change?
How do we trace a production failure across layers?
What data must never appear in logs?
```

Chapters 14–20 train around those questions.

---

## Recommended learning loop

Use the same engineering loop in every chapter:

```text
1. reproduce one concrete problem
2. write a failing test or explicit acceptance condition
3. make the smallest useful change
4. turn the evidence green
5. inspect logs / Network / database state
6. write down the trade-off
7. commit with a root-cause explanation
```

Do not try to make the entire repository “perfect” in one giant refactor.

The skill is learning to make changes that are:

```text
small
auditable
testable
reversible
explainable
```

---

## Reference engineering patterns already present

Current `main` contains several concrete patterns you can study:

### Reproducible AI modes

```text
mock
text
full
```

with explicit feature flags:

```text
ENABLE_RAG
ENABLE_ASR
ENABLE_TTS
```

### Runtime model configuration

Chat, Memory, Embedding, ASR, and TTS models are configured through the AI settings layer instead of being scattered through Views.

### Graceful speech decoupling

Real text chat does not require a working TTS WebSocket. Optional speech failure can degrade to text when the selected mode permits it.

### Shared token refresh

Axios and SSE share one refresh implementation and single-flight coordination instead of maintaining independent authentication truths.

### Real cancellation

```text
AbortController
  ↓
stream close
  ↓
Django generator cleanup
  ↓
cancel_event
```

is more meaningful than only hiding stale UI updates.

### Beginner diagnostics

```bash
python manage.py doctor
python manage.py seed_demo
npm run setup:vad
```

make first-run failures explicit and reproducible.

### Automated feedback

```text
Django tests
Node tests
structural grader
migration drift check
frontend quality/build
learning Docker build
```

run in GitHub Actions.

### Build-manifest integration

Django loads Vite's generated manifest instead of hard-coding changing hashed JS/CSS filenames.

### Data integrity

Friend relationships have a database-level uniqueness constraint, with migration logic that handles historical duplicates before applying the invariant.

### Retrieval evaluation

RAG retrieval is separated from Agent orchestration and can be evaluated independently with fixed cases and source expectations.

### Operational primitives

```text
GET /api/health/
X-Request-ID
```

provide the first building blocks for deployability and traceability.

---

## Chapter 14 — Testing / TDD

Main question:

> Who proves that a change did not break existing behavior?

Study:

```text
backend/web/tests.py
frontend/tests/singleFlight.test.js
scripts/grade.py
.github/workflows/ci.yml
```

Learn to separate:

```text
structural grading
unit behavior
integration behavior
browser E2E
manual acceptance
```

Lab: [Chapter 14](../labs/en/chapter-14-testing-tdd.md)

---

## Chapter 15 — DRF Engineering

Main question:

> How should an API express validation, conflicts, authentication, permissions, and failures without turning every View into ad-hoc parsing code?

Study:

```text
backend/web/serializers/account.py
account Views
older Character/Profile Views
```

Core concepts:

```text
Serializer
validation
HTTP status
machine error code
object-level authorization
OpenAPI-ready contracts
```

Lab: [Chapter 15](../labs/en/chapter-15-drf-engineering.md)

---

## Chapter 16 — Configuration and Providers

Main question:

> Why should switching models or disabling speech not require editing business code in multiple places?

Study:

```text
backend/web/ai/config.py
.env.example
manage.py doctor
```

Core concepts:

```text
feature flags
configuration vs secrets
provider abstraction
graceful degradation
mode-aware diagnostics
```

Lab: [Chapter 16](../labs/en/chapter-16-config-providers.md)

---

## Chapter 17 — Streaming and Cancellation

Main question:

> When the user clicks Stop, what actually stops?

Study:

```text
InputField.vue
streamApi.js
chat.py
Queue
cancel_event
```

Core concepts:

```text
AbortSignal
stream lifetime
generator cleanup
worker cancellation
sentinel
partial persistence
cancel vs timeout vs failure
```

Lab: [Chapter 17](../labs/en/chapter-17-stream-cancellation.md)

---

## Chapter 18 — Data and Security

Main question:

> Why are frontend checks and View-level checks not enough to guarantee data integrity and security?

Study:

```text
Friend UniqueConstraint
migration 0008
ownership filters
upload surfaces
SECURITY.md
```

Core concepts:

```text
DB invariant
transaction/race condition
object-level authorization
file validation
secret hygiene
prompt injection
Tool permissions
privacy lifecycle
```

Lab: [Chapter 18](../labs/en/chapter-18-data-security.md)

---

## Chapter 19 — RAG and Memory Evaluation

Main question:

> How do we prove RAG or Memory is better instead of saying “it feels better”?

Study:

```text
backend/web/documents/retrieval.py
scripts/eval_rag.py
evals/rag_cases.example.json
Friend.memory
```

Core concepts:

```text
retrieval vs generation evaluation
source provenance
citation integrity
structured memory
conflict resolution
negative memory cases
latency/cost measurement
```

Lab: [Chapter 19](../labs/en/chapter-19-rag-memory-eval.md)

---

## Chapter 20 — CI, Build, Deploy, Observability

Main question:

> Why is “works locally” far below the bar for maintainable software?

Study:

```text
.github/workflows/ci.yml
vite.config.js
backend/web/views/vite.py
backend/web/views/health.py
backend/web/middleware.py
Dockerfile.learning
```

Core concepts:

```text
CI as feedback/merge protection
build vs dev server
asset manifest
health checks
request correlation
structured logs
metrics
learning vs production container
browser E2E
bundle budgets
```

Lab: [Chapter 20](../labs/en/chapter-20-ci-deploy-observability.md)

---

## Graduation questions

After Chapter 20, you should be able to answer in your own words:

1. What do unit, integration, and end-to-end tests protect differently?
2. Why should HTTP status and an application `result` string not be the same thing?
3. Why do Serializers scale better than repeated `request.data.get(...).strip()` logic?
4. Why should provider/model configuration be decoupled from business Views?
5. How does cancellation propagate from browser → SSE → Django → worker?
6. Why can a DB unique constraint not be replaced by “check then create”?
7. How is Prompt Injection different from a normal web authorization bug?
8. How do you build a repeatable RAG evaluation set?
9. How should Memory represent source, time, confidence, and conflict?
10. Why should CI run before merge?
11. What is the difference between Build, Deploy, and Runtime Observability?
12. What is safe to expose in a health endpoint or logs?
13. Why is `Dockerfile.learning` intentionally not a production guarantee?
14. What would a browser E2E test add beyond current unit/behavior tests?

If you can answer these and implement one cross-layer feature with tests, documentation, and operational reasoning, you have learned an engineering method that transfers well beyond AiFriends.
