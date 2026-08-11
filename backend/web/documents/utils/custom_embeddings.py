"""OpenAI-compatible Embedding adapter used by LanceDB."""

import os

from langchain_core.embeddings import Embeddings
from openai import OpenAI

from web.ai.config import get_ai_settings


class CustomEmbeddings(Embeddings):
    def __init__(self):
        self.config = get_ai_settings()
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("API_BASE")
        )

    def embed_documents(self, texts):
        batch_size = 10
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = [text for text in texts[i:i + batch_size] if text.strip()]
            if not batch:
                continue
            response = self.client.embeddings.create(
                model=self.config.embedding_model,
                input=batch,
                dimensions=self.config.embedding_dimensions,
            )
            all_embeddings.extend([data.embedding for data in response.data])
        return all_embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]
