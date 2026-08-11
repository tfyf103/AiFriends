# Chapter 10 Lab：RAG、Embedding 与 LanceDB

## 本章目标

解决：

> 模型不知道你的私有资料、项目文档或最新内部知识怎么办？

不要把整份资料硬塞进每一次 Prompt。

本章实现：

```text
离线建库：
文档 → 切块 → Embedding → LanceDB

在线查询：
问题 → Embedding → similarity_search → Top K 文本 → Tool → LLM
```

---

## 历史检查点

```text
57f4c78c35313360065169c8ff008c77bba914a4  添加知识库 Tool
4c099063991521cdb55e58171919d2b623110d77  添加向量数据库建库代码
```

---

## TODO 1：先不用向量数据库做一次“笨办法”

创建一个 `data.txt`，写入几段不同主题文本。

尝试每次聊天都把整份文件放进 Prompt。

记录：

- 文档字符数
- Prompt 大小
- 当文档扩大 100 倍会发生什么

理解 RAG 的第一个动机：

> 只给模型当前问题最相关的资料，而不是所有资料。

---

## TODO 2：TextLoader

```python
loader = TextLoader(
    './web/documents/data.txt',
    encoding='utf-8',
)
documents = loader.load()
```

打印：

```python
print(documents)
```

### 验收

能解释 LangChain `Document` 至少包含：

```text
page_content
metadata
```

---

## TODO 3：文本切块

使用：

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

### 实验

分别试：

```text
chunk_size = 50
chunk_size = 500
chunk_size = 5000
```

观察 chunk 数量。

回答：

- 太小：语义可能被切碎
- 太大：检索结果包含太多无关信息、上下文浪费
- overlap：减少关键上下文恰好落在切分边界导致的信息丢失

---

## TODO 4：理解 Embedding

不要把 Embedding 当作“加密”。

它是：

```text
文本 → 一串浮点数向量
```

语义相似文本在向量空间中通常更接近。

实现 `CustomEmbeddings`：

```python
class CustomEmbeddings(Embeddings):
    def embed_documents(self, texts):
        ...

    def embed_query(self, text):
        ...
```

### 验收

打印：

```text
len(vector)
vector[:5]
```

确认项目当前设定是 1024 维。

---

## TODO 5：为什么有两个方法？

```text
embed_documents([...])
embed_query('...')
```

LangChain VectorStore 通过统一接口分别处理：

- 批量文档建库
- 单个用户查询

项目里的 query 实现可以复用 document embedding：

```python
return self.embed_documents([text])[0]
```

---

## TODO 6：批量 Embedding

项目使用：

```text
batch_size = 10
```

思考为什么不一定一次提交所有文本：

- API 单次 input 数限制
- token 限制
- 内存
- 超时
- 重试范围

### 主动实验

创建 25 个短文本，打印每次 batch 的长度，应看到类似：

```text
10
10
5
```

---

## TODO 7：写入 LanceDB

```python
db = lancedb.connect('./web/documents/lancedb_storage')

vector_db = LanceDB.from_documents(
    documents=texts,
    embedding=embeddings,
    connection=db,
    table_name='my_knowledge_base',
    mode='overwrite',
)
```

### 验收

- [ ] 本地生成 LanceDB storage
- [ ] row count 与有效 chunk 数基本对应
- [ ] 知道 `overwrite` 会重建表，不适合所有增量更新场景

---

## TODO 8：相似度检索

测试：

```python
docs = vector_db.similarity_search(
    '你的问题',
    k=3,
)
```

打印三个结果。

不要先让 LLM 回答，只评价：

> 检索出来的资料本身相关吗？

RAG 调试必须拆成：

```text
Retrieval 是否正确？
Generation 是否正确？
```

不能只看最终答案。

---

## TODO 9：封装为 LangChain Tool

```python
@tool
def search_knowledge_base(query: str) -> str:
    ...
```

返回：

```text
内容片段 1
内容片段 2
内容片段 3
```

把 Tool 加入：

```python
tools = [get_time, search_knowledge_base]
```

### 验收

问与知识库无关的问题时，不强迫调用 RAG。

问知识库专属内容时，Agent 触发 RAG Tool。

---

## TODO 10：做一个“检索失败案例”

故意写一个含义很模糊的问题，使检索拿到错误 chunk。

然后分别尝试：

- 改写 query
- 调整 chunk size
- 调整 k
- 改进文档结构

理解：RAG 不只是“换一个向量数据库”。数据准备和检索策略同样重要。

---

## 参考答案思路

RAG 的核心不是数据库品牌：

```text
Knowledge
  ↓ chunk
Chunks
  ↓ embedding
Vectors
  ↓ retrieve by semantic similarity
Relevant Context
  ↓
LLM
```

LanceDB 只是这个项目选择的 Vector Store。

---

## 常见错误

### 建库成功但查询报维度不一致

建库与查询必须使用兼容的 Embedding model/dimensions。

### 找不到 table

确认工作目录和：

```text
./web/documents/lancedb_storage
```

相对路径到底相对于哪个运行目录。

### 检索结果完全不相关

先不要怪 LLM。打印：

```python
for doc in docs:
    print(doc.page_content)
```

### data.txt 被 `.gitignore` 忽略

这是为了避免把本地/私有知识库内容默认提交。实验时自己创建即可。

---

## Challenge

设计一个简单的“引用来源”机制。

要求 RAG Tool 不只返回文本，还带：

```text
source
chunk index
```

然后让最终答案能告诉用户“信息来自哪个文档片段”。

思考：这为什么比让模型凭空回答更容易审计？
