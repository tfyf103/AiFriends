# Chapter 14 Lab: Testing, TDD, and Automated Failure Detection

🌐 **Language:** [中文](../chapter-14-testing-tdd.md) | **English**

## Goal

Upgrade from:

> “The page looks like it works.”

into:

> **“I have automated evidence that important behavior was not broken.”**

Current testing/feedback anchors include:

```text
backend/web/tests.py
frontend/tests/singleFlight.test.js
scripts/grade.py
.github/workflows/ci.yml
```

---

## TODO 1: Run backend tests

```bash
cd backend
python manage.py test web
```

### Understand the test database

Explain the difference between:

```text
test database
local development db.sqlite3
```

Tests should not corrupt your real development data.

### Current behavior areas covered

The maintained suite includes checks around:

- `AI_MODE` configuration;
- password hashing on registration;
- registration validation and duplicate usernames;
- invalid login credentials;
- refresh-cookie behavior;
- public health + request IDs;
- mock SSE chat without external AI;
- ASR feature flags;
- Friend database uniqueness;
- safe RAG source labels.

Do not memorize the list. Open `backend/web/tests.py` and map each test to the bug/invariant it protects.

---

## TODO 2: Run frontend tests

```bash
cd frontend
npm test
```

The first frontend tests intentionally use Node's built-in test runner to keep the dependency surface small.

Read:

```text
frontend/src/js/utils/singleFlight.js
frontend/tests/singleFlight.test.js
```

Explain:

> Why should ten simultaneous 401 responses normally share one refresh operation instead of firing ten refresh requests?

---

## TODO 3: Experience red → green

Temporarily break the single-flight behavior, for example by bypassing the shared pending promise.

Run:

```bash
npm test
```

You should see a concurrency test fail.

Restore the implementation until the test becomes green again.

### TDD lesson

```text
failing evidence
  ↓
small implementation change
  ↓
passing evidence
  ↓
refactor with protection
```

TDD is not “write tests because tests are good.” It is a feedback loop for designing and changing behavior.

---

## TODO 4: Understand the structural grader

From the repository root:

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 20
```

The grader checks whether expected course structures/concepts exist.

It is **not** proof that runtime behavior is correct.

Be able to distinguish:

```text
structural grader
unit test
integration test
end-to-end test
manual acceptance test
```

---

## TODO 5: Write a regression test from a real bug

Choose one historical/real class of bug:

```text
SSE refresh succeeds but stale access token is reused
registration missing fields crashes
ASR disabled but code still opens WSS
mock mode unexpectedly calls a real model
Friend duplicate relationship appears
absolute server path leaks through RAG source metadata
```

Workflow:

1. write a test that fails before the fix;
2. reproduce the root cause;
3. implement the smallest fix;
4. make the test green;
5. describe the root cause in the commit message.

---

## TODO 6: Test boundaries, not implementation trivia

Bad test style:

```text
assert a private helper was called exactly twice
```

when the real contract is:

```text
one refresh request is shared by concurrent callers
```

Prefer externally meaningful invariants where possible.

Ask:

```text
What behavior would a user/maintainer notice if this broke?
What is the smallest stable interface I can assert?
```

---

## TODO 7: Understand Mock mode as a testability feature

CI runs core chat behavior without spending external LLM/TTS credits.

Explain why this matters:

- deterministic responses;
- no provider outage dependency;
- no secret required in contributor PRs;
- fast, reproducible tests;
- still exercises real authentication/Friend/SSE/persistence paths.

Also explain the limitation:

> Mock passing does not prove a third-party provider integration is healthy.

---

## Acceptance

- [ ] You can run backend tests.
- [ ] You can run frontend tests.
- [ ] You can explain why Mock mode is useful in CI.
- [ ] You deliberately created and fixed a failing test.
- [ ] You added one regression test for a real bug/invariant.
- [ ] You can explain why “all tests pass” never means “the product has no bugs.”
- [ ] You can distinguish structural grading from behavior testing.

---

## Challenge

Add tests around Vite manifest resolution (`get_vite_entry()`), including cases such as:

```text
manifest missing
index.html entry exists
only an isEntry candidate exists
0 / 1 / multiple CSS files
malformed manifest
```

Then run the tests through CI.

Write one paragraph explaining which failures belong to:

```text
unit tests
build smoke tests
browser E2E
```

and why one layer alone is insufficient.
