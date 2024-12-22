from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_qa_chain(retriever):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.LLM_MODEL
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
