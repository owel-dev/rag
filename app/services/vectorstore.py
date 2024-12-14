# vectorstore.py
from typing import List

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core import settings

# OpenAI Embeddings 인스턴스 생성
openai_embeddings = OpenAIEmbeddings()


def get_vectorstore():
    client_settings = Settings(
        chroma_api_impl="chromadb.api.fastapi.FastAPI",
        chroma_server_host=settings.CHROMA_HOST,
        chroma_server_http_port=settings.CHROMA_PORT
    )

    # Chroma 벡터스토어 초기화
    vectorstore = Chroma(
        collection_name="pdf_docs",
        embedding_function=openai_embeddings,  # 래퍼를 embedding_function으로 전달
        client_settings=client_settings
    )
    return vectorstore


# 필요하다면 전역 변수로 인덱스 초기화
vectorstore = get_vectorstore()
