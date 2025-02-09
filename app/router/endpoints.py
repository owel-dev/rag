import json

from fastapi import APIRouter, File, UploadFile, Depends, Form
from langchain_core.documents import Document

from app.dependencies import get_ocr_engine, IOCR
from app.schemas.request import QueryRequest
from app.services.llm_chain import get_rewriting_chain, get_keyword_chain, get_retrieval_qa_chain
from app.services.vectorstore import get_vectorstore
from app.services.ocr import extract_text_from_pdf
from app.services.text_preprocessing import split_text_into_chunks

router = APIRouter()

vectorstore = get_vectorstore()


@router.post("/query")
async def query(request: QueryRequest):
    # rewritten = get_rewriting_chain().run(query=request.query)
    # print("RewritingChain output_keys:", rewritten)

    # keywords = get_keyword_chain().run(query=request.query)
    # arr = [word.strip() for word in keywords.split(",")]
    # print("KeywordChain output_keys:", arr)


    # recognized_keywords = []
    # threshold = 0.8  # 예시로 0.8 설정


    # for kw in arr:
    #     results = vectorstore.similarity_search_with_score(kw, k=1)
    #     if results:
    #         doc, score = results[0]
    #         if score > threshold:
    #             recognized_keywords.append(kw)
    # print("인식된 키워드(임계값 초과):", recognized_keywords)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # (1) 직접 검색된 문서(청크) 가져오기
    relevant_docs = retriever.get_relevant_documents(request.query)

    # (2) 문서 메타데이터에서 act, article 정보 뽑아서 설명 텍스트 구성
    explanation_list = []
    for i, doc in enumerate(relevant_docs, start=1):
        act = doc.metadata.get("act", "알 수 없는 법")
        article = doc.metadata.get("article", "알 수 없는 조항")
        explanation_list.append(f"{i}. {act} {article}")

    # 예: "다음은 검색된 문서의 법령/조항 정보입니다:\n1. 소방기본법 19조\n2. 소방시설공사엄범 2조"
    if explanation_list:
        explanation_text = (
                "다음은 검색된 문서의 법령/조항 정보입니다:\n" + "\n".join(explanation_list)
        )
    else:
        explanation_text = "검색된 문서에서 별도의 법령/조항 정보가 확인되지 않았습니다."

    # (3) RetrievalQA를 이용해 실제 질의/응답 수행
    answer = get_retrieval_qa_chain(retriever).run(query=request.query)

    # (4) 최종 응답: answer + 메타데이터 기반 설명
    return {
        "answer": answer,
        "explanation": explanation_text
    }


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...),
                     act: str = Form(...),
                     ocr_engine: IOCR = Depends(get_ocr_engine)):
    content = await file.read()
    full_text = extract_text_from_pdf(content, ocr_engine, file.filename)
    docs = split_text_into_chunks(full_text, act)
    vectorstore.add_documents(docs)
    return {"status": "success", "num_chunks": len(docs)}
