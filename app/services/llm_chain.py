from typing import List

from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.sequential import SequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI

from app.core.config import settings


# 공통 LLM(ChatOpenAI) 설정
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.LLM_MODEL
    )


# 사용자 질문을 검색에 친화적인 문장으로 재작성하는 LLMChain
def get_rewriting_chain() -> LLMChain:
    prompt = PromptTemplate(
        input_variables=["query"],
        template=(
            "당신은 전문적인 어시스턴트입니다. 사용자의 질문은 비격식적이거나 불필요한 정보가 포함될 수 있습니다.\n"
            "다음 사용자 질문을 간결하고 검색에 적합한 형식으로 재작성해주세요:\n\n{query}\n\n"
            "재작성된 질문은 원래의 핵심 의미를 유지하면서, 검색 작업에 더 효과적으로 사용할 수 있도록 구성해주세요."
        )
    )
    return LLMChain(
        llm=get_llm(),
        prompt=prompt,
        output_key="result",
        verbose=True
    )


# 사용자 질문에서 키워드를 추출하는 LLMChain
def get_keyword_chain() -> LLMChain:
    prompt = PromptTemplate(
        input_variables=["query"],
        template=(
            "사용자 질문: {query}\n\n"
            "위 문장에서 핵심 키워드를 추출해줘.\n"
            "- 핵심 단어(명사/명사구/주제어 등)만 뽑아줘.\n"
            "- 중요도가 낮은 단어(조사, 접속사 등)는 제거.\n"
            "- 키워드는 중복 없이.\n"
            "최종 결과는 쉼표(,)로 구분된 형태로만 출력해."
        )
    )
    return LLMChain(
        llm=get_llm(),
        prompt=prompt,
        output_key="result",  # 다음 단계가 이 값을 query로 받아 검색하도록
        verbose=True
    )


# 키워드기반으로 벡터 검색하고, QA를 수행하는 RetrievalQA 체인.
def get_retrieval_qa_chain(retriever: BaseRetriever) -> RetrievalQA:
    llm = get_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        verbose=True,
        input_key="query",  # 이 체인이 입력받을 필드명
        output_key="result"  # 최종 결과를 담아 반환할 필드명
    )
    return qa_chain
