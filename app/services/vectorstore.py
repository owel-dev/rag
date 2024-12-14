# vectorstore.py
from typing import List
from chromadb import Client
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# OpenAI Embeddings 인스턴스 생성
openai_embeddings = OpenAIEmbeddings()


class ChromaEmbeddingFunction:
    def __init__(self, embeddings: OpenAIEmbeddings):
        self.embeddings = embeddings

    def __call__(self, input: List[str]) -> List[List[float]]:
        # Chroma가 직접 callable로 호출할 때 사용
        return self.embeddings.embed_documents(input)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Chroma가 embedding_function.embed_documents를 호출할 경우 대비
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        # 필요하다면 embed_query도 지원
        return self.embeddings.embed_query(text)


def get_vectorstore():
    client = Client(Settings(
        chroma_server_host="chroma",
        chroma_server_http_port=8000,
    ))
    # 래핑된 EmbeddingFunction 인스턴스
    chroma_embedding_func = ChromaEmbeddingFunction(openai_embeddings)

    # Chroma 벡터스토어 초기화
    vectorstore = Chroma(
        collection_name="pdf_docs",
        embedding_function=chroma_embedding_func,  # 래퍼를 embedding_function으로 전달
        client=client
    )
    return vectorstore


# 필요하다면 전역 변수로 인덱스 초기화
vectorstore = get_vectorstore()
