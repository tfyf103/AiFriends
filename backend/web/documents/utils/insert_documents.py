"""
把原始文本资料写入 LanceDB 的“建库脚本”。

RAG 一般分成两个完全不同的阶段：

A. 建库阶段（通常离线执行）
   原始文档
     -> Loader 读取
     -> Text Splitter 切块
     -> Embedding 转向量
     -> Vector DB 保存

B. 查询阶段（用户聊天时实时执行）
   用户问题
     -> Embedding
     -> Vector DB 相似度搜索
     -> 取回相关文本
     -> LLM 根据文本回答

这个文件负责 A；chat/graph.py 中的 search_knowledge_base() 负责 B。
理解“建库”和“检索”是两个阶段，是学懂 RAG 的第一步。
"""

import lancedb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter

from web.documents.utils.custom_embeddings import CustomEmbeddings


def insert_documents():
    """
    读取 ./web/documents/data.txt，切分、向量化并写入本地 LanceDB。

    当前 mode='overwrite'，所以每执行一次都会重建 my_knowledge_base 表。
    这对教学和小型 Demo 很直观，但真实生产系统通常会设计增量更新策略。
    """

    # ------------------------------------------------------------------
    # Step 1：加载原始文档
    # ------------------------------------------------------------------
    # TextLoader 会把文本文件转换成 LangChain Document 对象。
    loader = TextLoader(
        './web/documents/data.txt',
        encoding='utf-8',
    )
    documents = loader.load()

    # ------------------------------------------------------------------
    # Step 2：切块 Chunking
    # ------------------------------------------------------------------
    # 为什么不能直接把一整份大文档作为一个向量？
    # 因为用户通常只问文档中的一个局部问题。切成较小片段后，检索粒度更细。
    #
    # chunk_size=500：每个文本块大约最多 500 个字符；
    # chunk_overlap=50：相邻块保留约 50 个字符重叠，降低“关键信息刚好被切断”的概率。
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    texts = text_splitter.split_documents(documents)

    print(f"已切分成 {len(texts)} 个片段。")

    # ------------------------------------------------------------------
    # Step 3：准备 Embedding 模型
    # ------------------------------------------------------------------
    # CustomEmbeddings 会在 LanceDB 写入前，把每个 Document.page_content 转成 1024 维向量。
    embeddings = CustomEmbeddings()

    # ------------------------------------------------------------------
    # Step 4：连接本地 LanceDB
    # ------------------------------------------------------------------
    # LanceDB 可以直接把数据库保存成项目目录下的本地文件，适合学习和原型开发。
    db = lancedb.connect('./web/documents/lancedb_storage')

    # ------------------------------------------------------------------
    # Step 5：向量化并写入数据库
    # ------------------------------------------------------------------
    vector_db = LanceDB.from_documents(
        documents=texts,
        embedding=embeddings,
        connection=db,
        table_name='my_knowledge_base',

        # overwrite = 如果表已存在就重建。
        # 注意：这意味着旧数据会被覆盖。
        mode='overwrite',
    )

    print(f"已插入 {vector_db._table.count_rows()} 行数据。")
