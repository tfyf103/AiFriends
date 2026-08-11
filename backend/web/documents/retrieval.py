"""Reusable RAG retrieval layer.

Keeping retrieval outside the LangGraph Tool has two benefits:

1. the Agent remains responsible for orchestration, not vector-store plumbing;
2. Chapter 19 can evaluate retrieval directly without asking the LLM to generate an answer.
"""

from __future__ import annotations

import lancedb
from langchain_community.vectorstores import LanceDB
from langchain_core.documents import Document

from web.documents.utils.custom_embeddings import CustomEmbeddings


def get_vector_store() -> LanceDB:
    connection = lancedb.connect('./web/documents/lancedb_storage')
    return LanceDB(
        connection=connection,
        embedding=CustomEmbeddings(),
        table_name='my_knowledge_base',
    )


def search_documents(query: str, k: int = 3) -> list[Document]:
    """Return raw Documents so callers can inspect content *and* metadata."""
    return get_vector_store().similarity_search(query, k=k)


def document_source(document: Document) -> str:
    """Choose a stable human-readable source label from LangChain metadata."""
    metadata = document.metadata or {}
    return str(
        metadata.get('source')
        or metadata.get('file_path')
        or metadata.get('filename')
        or 'unknown-source'
    )


def format_documents_for_tool(documents: list[Document]) -> str:
    """Format retrieved evidence with explicit source labels for the LLM/user."""
    if not documents:
        return '知识库没有找到相关资料。'

    blocks = []
    for index, document in enumerate(documents, start=1):
        blocks.append(
            f'资料 {index}\n'
            f'来源：{document_source(document)}\n'
            f'内容：{document.page_content}'
        )
    return '\n\n'.join(blocks)
