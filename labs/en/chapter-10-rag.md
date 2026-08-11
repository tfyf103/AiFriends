# Chapter 10 Lab: RAG, Embeddings, and LanceDB

🌐 **Language:** [简体中文](../chapter-10-rag.md) | **English**

## Goal

Solve this problem:

> What if the model does not know your private documents, project-specific knowledge, or information outside its training context?

Do not paste the entire knowledge base into every prompt.

Build two separate paths:

```text
Offline indexing:
Document → Chunk → Embedding → LanceDB

Online retrieval:
Question → Embedding → similarity search → Top-k evidence → Tool → LLM
```

The current project also separates retrieval into `backend/web/documents/retrieval.py`, which makes RAG easier to evaluate independently from the Agent.

---

## Historical checkpoints

Useful project-history commits:

```text
57f4c78c35313360065169c8ff008c77bba914a4  add knowledge-base Tool
4c099063991521cdb55e58171919d2b623110d77  add vector-database indexing code
```

Use them to understand the evolution, then compare with the current retrieval/evaluation implementation.

---

## TODO 1: Try the intentionally bad approach first

Create a local `data.txt` with several topics.

Imagine placing the entire file in every prompt.

Record:

- number of characters/chunks;
- approximate prompt size;
- what happens conceptually if the document becomes 100× larger;
- whether every paragraph is relevant to every question.

The first RAG motivation is:

> Give the model the evidence relevant to the current question, not the entire corpus every time.

---

## TODO 2: Load documents

A simple LangChain loader looks like:

```python
loader = TextLoader(
    '...',
    encoding='utf-8',
)
documents = loader.load()
```

Inspect the result.

### Acceptance

You can explain that a `Document` contains at least:

```text
page_content
metadata
```

Metadata matters later when you want to preserve safe source/citation information.

---

## TODO 3: Split text into chunks

Experiment with:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

Then compare:

```text
chunk_size = 50
chunk_size = 500
chunk_size = 5000
```

Record the number and shape of chunks.

### Explain the trade-off

Too small:

```text
meaning may be fragmented
```

Too large:

```text
retrieved chunks contain more irrelevant content
context/token budget is wasted
```

Overlap:

```text
reduces information loss around chunk boundaries
```

There is no universal best chunk size; it depends on document structure and retrieval goals.

---

## TODO 4: Understand embeddings

Embedding is not encryption.

It is a transformation like:

```text
text
 ↓
vector of floating-point numbers
```

Semantically related text tends to map to nearby regions in the embedding space.

AiFriends uses a custom LangChain `Embeddings` implementation with methods such as:

```python
class CustomEmbeddings(Embeddings):
    def embed_documents(self, texts):
        ...

    def embed_query(self, text):
        ...
```

### Acceptance

For a test vector, inspect:

```python
len(vector)
vector[:5]
```

The current project configuration exposes embedding model/dimensions through environment/runtime settings rather than requiring hard-coded values in retrieval business logic.

---

## TODO 5: Explain document vs query embedding APIs

Why does the interface expose both:

```text
embed_documents([...])
embed_query('...')
```

Because the vector-store workflow has two operational shapes:

```text
batch document indexing
single query retrieval
```

An implementation may reuse lower-level provider calls, but the semantic roles remain different.

---

## TODO 6: Batch embeddings

Imagine indexing 25 chunks with a batch size of 10.

Your instrumentation should show something like:

```text
10
10
5
```

Explain why batching matters:

- provider input limits;
- token limits;
- memory usage;
- request timeouts;
- retry scope;
- rate limits/cost visibility.

### Deliberate failure

Try an unrealistically large batch in a controlled experiment and observe whether the failure comes from provider input limits, timeout, or memory pressure.

Do not keep the broken configuration.

---

## TODO 7: Write vectors into LanceDB

Conceptually:

```python
db = lancedb.connect(...)

vector_db = LanceDB.from_documents(
    documents=texts,
    embedding=embeddings,
    connection=db,
    table_name='my_knowledge_base',
    mode='overwrite',
)
```

### Acceptance

- [ ] local LanceDB storage exists;
- [ ] row count roughly corresponds to valid chunks;
- [ ] you understand what `overwrite` means;
- [ ] you can explain why overwrite is not a universal incremental-indexing strategy.

The current project uses stable paths based on Django settings rather than assuming an arbitrary working directory.

---

## TODO 8: Test retrieval before generation

Run a semantic query conceptually like:

```python
docs = vector_db.similarity_search(
    'your question',
    k=3,
)
```

Print the returned Documents.

Do **not** ask the LLM to answer yet.

Evaluate:

> Are these retrieved chunks actually relevant evidence for the question?

This is one of the most important RAG debugging habits:

```text
Retrieval quality?
        ↓
Generation quality?
```

Do not collapse both into “the final answer was bad.”

---

## TODO 9: Use the current retrieval abstraction

The current project extracts retrieval into:

```text
backend/web/documents/retrieval.py
```

The useful abstraction is conceptually:

```text
search_documents(query, k)
```

instead of embedding/vector-store construction being buried inside the Agent node.

### Acceptance

You can explain why this improves:

- testability;
- evaluation;
- provider replacement;
- debugging;
- future citation/UI work.

---

## TODO 10: Preserve safe source metadata

A retrieved Document should be able to carry source information, but do not expose absolute server filesystem paths directly to users.

The current project normalizes source labels.

### Acceptance

Given a source such as:

```text
/srv/app/private/path/data.txt
```

user-facing evidence should expose a safe label such as:

```text
data.txt
```

not the full server path.

Explain why this is both a product and security/privacy concern.

---

## TODO 11: Wrap retrieval as a Tool

Conceptually:

```python
@tool
def search_knowledge_base(query: str) -> str:
    ...
```

The Tool should return useful evidence, ideally including safe source labels.

Register it only when RAG is enabled:

```env
ENABLE_RAG=true
```

### Acceptance

- [ ] unrelated small talk does not have to call RAG;
- [ ] knowledge-base-specific questions can trigger the RAG Tool;
- [ ] disabling RAG removes that external dependency from the runtime path.

---

## TODO 12: Run retrieval-only evaluation

AiFriends includes an example evaluation set:

```text
evals/rag_cases.example.json
```

and runner:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

The runner checks retrieval expectations such as keywords/source labels before asking whether a generated answer is fluent.

### Acceptance

You can explain the difference between:

```text
retrieval failure
vs
generation/faithfulness failure
```

This decomposition is the beginning of real RAG evaluation.

---

## TODO 13: Create a retrieval failure case

Write an ambiguous query that retrieves the wrong chunk.

Then change **one variable at a time**:

- query wording;
- chunk size;
- chunk overlap;
- `k`;
- document structure/metadata;
- embedding model/dimensions if justified.

Record the retrieval result after each change.

### Important lesson

RAG quality is not “choose a vector database and you are done.”

Data preparation, chunking, embedding choice, retrieval strategy, metadata, and evaluation all matter.

---

## Reference mental model

RAG is fundamentally:

```text
Knowledge
  ↓ chunk
Chunks
  ↓ embedding
Vectors
  ↓ semantic retrieval
Relevant evidence
  ↓
LLM
```

LanceDB is the Vector Store used by this project; it is not the definition of RAG.

---

## Common errors

### Indexing works, query fails with dimension mismatch

Indexing and querying must use compatible embedding model/dimensions.

### LanceDB table/storage cannot be found

Inspect the resolved storage path. Do not assume a relative path means the same thing from every working directory.

### Retrieval is irrelevant

Do not blame the LLM yet.

Print:

```python
for doc in docs:
    print(doc.page_content)
    print(doc.metadata)
```

### Local knowledge data is ignored by Git

That may be intentional so private/local knowledge is not committed by default.

### Source leaks a server path

Normalize metadata before returning it to the Agent/user-facing layer.

### RAG is enabled but provider config is missing

Use:

```bash
cd backend
python manage.py doctor
```

and inspect feature flags/config rather than debugging the Agent loop first.

---

## Challenge

Design a first-class citation event for the chat stream.

Instead of only putting source text inside the LLM Tool result, imagine an SSE event such as:

```json
{
  "citation": {
    "source": "data.txt",
    "chunk": 3
  }
}
```

Then answer:

1. Which layer should create this structured citation?
2. Should the LLM be trusted to invent the source label?
3. How would the frontend render citations separately from normal text?
4. How would you test that server filesystem paths are never exposed?
5. How would retrieval evaluation verify source correctness?

This is a bridge from “RAG demo” to auditable AI product behavior.

---

Previous: [Chapter 08 — LangGraph Tool Calling](./chapter-08-langgraph-tools.md)  
Next: [Chapter 13 — Full-System Capstone](./chapter-13-capstone.md)
