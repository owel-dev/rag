from chromadb.config import Settings
from fastapi import Depends
from langchain_chroma import Chroma

from app.core import settings
from app.dependencies import get_embedding_function


def get_vectorstore():
    client_settings = Settings(
        chroma_api_impl="chromadb.api.fastapi.FastAPI",
        chroma_server_host=settings.VECTORSTORE_HOST,
        chroma_server_http_port=settings.VECTORSTORE_PORT
    )

    # Chroma 벡터스토어 초기화
    vectorstore = Chroma(
        collection_name="pdf_docs",
        embedding_function=get_embedding_function(),  # 래퍼를 embedding_function으로 전달
        client_settings=client_settings
    )

    return vectorstore
