from fastapi import APIRouter, File, UploadFile
from app.models.request import QueryRequest
from app.services.llm_chain import get_qa_chain
from app.services.embeddings import get_embedding_function
from app.services.vectorstore import get_vectorstore
from app.services.ocr import extract_text_from_pdf
from app.utils.text_preprocessing import split_text_into_chunks

router = APIRouter()

embedding_function = get_embedding_function()
vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
qa_chain = get_qa_chain(retriever)


@router.post("/query")
async def query(request: QueryRequest):
    answer = qa_chain.invoke(request.query)
    return {"answer": answer}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    full_text = extract_text_from_pdf(content)
    docs = split_text_into_chunks(full_text)
    vectorstore.add_documents(docs)
    return {"status": "success", "num_chunks": len(docs)}
