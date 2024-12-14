from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_qa_chain(retriever):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
        model_name="gpt-4o-mini"  # 실제 사용 가능한 모델명으로 교체
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
