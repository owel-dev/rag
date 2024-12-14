import os
from functools import lru_cache

# 토크나이저 병렬화 비활성화
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from app.core import settings


@lru_cache()
def get_openai_embedding_function():
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


@lru_cache()
def get_huggingface_embedding_function():
    return HuggingFaceEmbeddings(model_name=settings.VECTORSTORE_EMBED_MODEL)


def get_embedding_function():
    if settings.VECTORSTORE_EMBED_PROVIDER == "hugging-face":
        return get_huggingface_embedding_function()
    else:
        return get_openai_embedding_function()
