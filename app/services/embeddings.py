from langchain_openai import OpenAIEmbeddings


# 예: OpenAI Embedding 사용
# 실제로는 settings.OPENAI_API_KEY 필요할 수 있음
def get_embedding_function():
    # OpenAI Embeddings or HuggingFaceEmbeddings 중 택 1
    # return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    return OpenAIEmbeddings()
