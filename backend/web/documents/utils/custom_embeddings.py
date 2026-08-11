"""
自定义 Embedding 适配器。

RAG 中最容易让初学者困惑的点之一是：
“为什么文本能放进向量数据库，还能做相似度搜索？”

关键就在 Embedding：它把一段文字转换成一串浮点数（向量）。
语义相近的文本，在向量空间里通常也更接近。

本项目用同一个 CustomEmbeddings 同时处理：

1. 建库时的文档片段：embed_documents([...])
2. 用户查询：embed_query("问题")

只有两边使用一致/兼容的向量表示，LanceDB 才能正确比较相似度。
"""

import os

from langchain_core.embeddings import Embeddings
from openai import OpenAI


class CustomEmbeddings(Embeddings):
    """
    把 OpenAI-compatible Embedding API 包装成 LangChain 认识的 Embeddings 接口。

    为什么要继承 Embeddings？
    LangChain 的 VectorStore 不想关心你背后使用的是哪家模型供应商，
    它只要求对象至少能做到两件事：

        embed_documents(list[str]) -> list[list[float]]
        embed_query(str) -> list[float]

    这样 LanceDB 等组件就可以统一调用。
    """

    def __init__(self):
        # OpenAI Python SDK 同样支持 OpenAI-compatible API。
        # API_KEY 和 API_BASE 从 .env 中读取，避免把密钥写进源码。
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("API_BASE")
        )

    def embed_documents(self, texts):
        """
        把多段文本批量转换成向量。

        参数示例：
            ["第一段文字", "第二段文字"]

        返回示意：
            [
                [0.01, -0.22, ...],
                [0.15,  0.08, ...],
            ]

        项目当前每批最多发送 10 段，避免一次请求塞入过多文本。
        """
        batch_size = 10
        all_embeddings = []

        # range(0, len(texts), batch_size) 会得到 0、10、20……
        # 每轮切出一小批文本发送给 Embedding API。
        for i in range(0, len(texts), batch_size):
            batch = texts[i: i + batch_size]

            # 空字符串没有检索价值，也可能被模型接口拒绝，所以提前过滤。
            batch = [text for text in batch if text.strip()]
            if not batch:
                continue

            response = self.client.embeddings.create(
                model="text-embedding-v4",
                input=batch,

                # 当前项目显式要求 1024 维向量。
                # 建库和查询时必须保持一致，否则无法在同一向量表中比较。
                dimensions=1024
            )

            # API 返回 data 列表，每个 data.embedding 就是一段文本对应的向量。
            all_embeddings.extend([
                data.embedding
                for data in response.data
            ])

        return all_embeddings

    def embed_query(self, text):
        """
        把“单个查询字符串”转换成一个向量。

        为避免重复写 API 调用逻辑，这里直接复用 embed_documents，
        只传一个元素，然后取返回列表中的第 0 个向量。
        """
        return self.embed_documents([text])[0]
