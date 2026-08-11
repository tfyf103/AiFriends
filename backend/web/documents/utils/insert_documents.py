"""Build the local LanceDB knowledge base used by AiFriends RAG.

This is the offline/indexing half of RAG. Online retrieval lives in
``web.documents.retrieval`` so it can be evaluated independently from the Agent.
"""

from pathlib import Path

import lancedb
from django.conf import settings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter

from web.documents.utils.custom_embeddings import CustomEmbeddings


def insert_documents():
    source_path = Path(settings.BASE_DIR) / 'web' / 'documents' / 'data.txt'
    storage_path = Path(settings.BASE_DIR) / 'web' / 'documents' / 'lancedb_storage'

    if not source_path.exists():
        raise FileNotFoundError(
            f'知识库文件不存在：{source_path}。请先创建 data.txt。'
        )

    loader = TextLoader(str(source_path), encoding='utf-8')
    documents = loader.load()

    # Do not persist an absolute machine-specific path into metadata. A stable
    # source label is easier to show as a citation and safer to expose to users.
    for document in documents:
        document.metadata['source'] = source_path.name

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = text_splitter.split_documents(documents)
    print(f'已切分成 {len(chunks)} 个片段。')

    vector_db = LanceDB.from_documents(
        documents=chunks,
        embedding=CustomEmbeddings(),
        connection=lancedb.connect(str(storage_path)),
        table_name='my_knowledge_base',
        mode='overwrite',
    )

    print(f'已插入 {vector_db._table.count_rows()} 行数据。')
    return vector_db
