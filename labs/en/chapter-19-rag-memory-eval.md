# Chapter 19 Lab: RAG Evaluation, Source Citations, and Structured Memory

🌐 **Language:** [中文](../chapter-19-rag-memory-eval.md) | **English**

## Goal

Upgrade from:

> “RAG retrieves something and Memory produces a summary.”

into:

> **“I can measure whether retrieval/memory actually improved, and I can explain where evidence or remembered facts came from.”**

Current AiFriends already separates retrieval into:

```text
backend/web/documents/retrieval.py
```

and provides a retrieval-only evaluation runner:

```text
scripts/eval_rag.py
evals/rag_cases.example.json
```

This chapter expands that engineering mindset.

---

## TODO 1: Build a fixed RAG evaluation set

Create your own:

```text
evals/rag_cases.json
```

Each case should contain at least:

```json
{
  "question": "Which vector database does AiFriends use?",
  "expected_keywords": ["LanceDB"],
  "expected_source": "data.txt"
}
```

Prepare a balanced set, for example:

```text
10 questions that should retrieve knowledge
5 questions that should not need the KB
5 ambiguous/confusable questions
```

### Why fixed cases?

If you change chunking, embeddings, or retrieval code and only ask new ad-hoc questions every time, you cannot compare versions reproducibly.

---

## TODO 2: Evaluate retrieval separately from generation

Do not judge only the final LLM answer.

Split the system:

```text
Question
  ↓
Retrieval
  ↓
Did we fetch the correct evidence?

Evidence + Question
  ↓
Generation
  ↓
Did the model use the evidence faithfully?
```

Start with simple metrics:

```text
keyword hit
source hit
Recall@k
manual relevance score
manual/automated faithfulness checks
```

### Run the current retrieval evaluator

After real RAG is configured:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

The current runner intentionally avoids requiring the generation model to evaluate basic retrieval quality.

---

## TODO 3: Inspect source handling

Current retrieval helpers normalize document source labels so absolute server filesystem paths are not exposed as citations.

Read:

```text
backend/web/documents/retrieval.py
```

### Acceptance

You can explain why this is safer:

```text
/Users/alice/private/server/path/data.txt  ❌
data.txt                                   ✅
```

Source metadata should identify useful evidence without leaking deployment filesystem details.

---

## TODO 4: Design first-class citation data

Today the Agent receives source-aware evidence, but a future UI should not rely on the LLM inventing citation text.

Design an event/response model such as:

```json
{
  "type": "citation",
  "source": "guide.md",
  "chunk_id": "guide-003",
  "text": "..."
}
```

or an equivalent structured schema.

### Key rule

> Citation metadata comes from retrieved `Document.metadata`, not from a free-form model guess.

---

## TODO 5: Compare retrieval parameters with data

Record results for variants such as:

```text
k = 3 vs 5
chunk_size = 300 vs 500 vs 800
chunk_overlap = 0 vs 50 vs 100
embedding model/dimensions A vs B
query rewrite on/off
```

Measure:

```text
retrieval hit rate
source hit rate
latency
embedding calls/cost
context size
```

Do not declare one configuration “better” based on one memorable demo question.

---

## TODO 6: Design structured long-term memory

Current persisted memory is a free-text field:

```text
Friend.memory
```

Design a structured representation:

```json
{
  "profile": [],
  "preferences": [],
  "relationships": [],
  "goals": [],
  "events": []
}
```

Each memory item can carry provenance:

```json
{
  "value": "Prefers tea",
  "source_message_id": 123,
  "timestamp": "...",
  "confidence": 0.95,
  "status": "active"
}
```

### Explain the benefit

A structured memory can be:

- queried by category;
- updated selectively;
- audited back to source messages;
- conflict-resolved explicitly;
- filtered for privacy/sensitivity.

### Explain the cost

It also adds:

- schema migration complexity;
- validation requirements;
- LLM structured-output failures;
- versioning/conflict policy;
- more code than one summary string.

---

## TODO 7: Handle memory conflicts

Simulate:

```text
Day 1:  I love coffee.
Day 10: I stopped drinking coffee; I prefer tea now.
```

Design a policy:

```text
overwrite old value?
keep history?
mark old item superseded?
store effective_from timestamps?
ask model to resolve?
require explicit user correction?
```

### Acceptance

Your current memory view can answer:

> Why is “tea” the active preference now?

with a traceable source/history explanation.

---

## TODO 8: Build a Memory evaluation set

Include conversations for:

```text
stable preference
short-lived emotion
one-off event
conflicting fact
negation
uncertain statement
sensitive information
explicit request to forget
```

Evaluate:

```text
Did it remember what it should?
Did it avoid storing what it should not?
Did conflicts update correctly?
Did it invent anything?
Can each active fact be traced to evidence?
```

---

## TODO 9: Evaluate utility and privacy together

A memory system that stores everything may score well on recall while being terrible for privacy.

Define policies such as:

```text
never persist secrets/tokens
avoid unnecessary sensitive attributes
allow reset/delete
track source
expire low-confidence/transient facts
```

Then include negative test cases:

> **“Should NOT be remembered.”**

---

## TODO 10: Record cost and latency

Track at least:

```text
retrieval latency
embedding latency
LLM latency
input tokens
output tokens
memory-update tokens
number of retrieved chunks
```

Compare memory update policies:

```text
every 5 Messages
every 10 Messages
token threshold
fact-triggered update
```

A better memory/RAG system should be evaluated on both quality and operational cost.

---

## Acceptance

- [ ] You maintain a fixed RAG evaluation set.
- [ ] Retrieval and generation are evaluated separately.
- [ ] Sources come from real retrieval metadata.
- [ ] Absolute server paths are not exposed as citations.
- [ ] You designed a structured memory schema with provenance.
- [ ] At least one memory conflict has an explicit resolution policy.
- [ ] You test examples that should **not** be remembered.
- [ ] You compare RAG/Memory configurations with measured data.

---

## Challenge: Build a RAG Debug Panel

Create a developer-only page showing:

```text
query
query embedding dimensions
top-k chunks
score/distance
source
chunk id
final context/prompt
final answer
retrieval latency
generation latency
tokens
```

Then add a “compare two configurations” mode.

The goal is to turn RAG from a black box into an observable, testable subsystem.
