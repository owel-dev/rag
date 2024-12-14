from fastapi import APIRouter, File, UploadFile
from app.services.ocr import extract_text_from_pdf
from app.services.embeddings import get_embedding_function
from app.services.vectorstore import get_vectorstore
from app.utils.text_preprocessing import split_text_into_chunks

router = APIRouter()

# 전역/싱글톤 처리가 필요하다면 DI나 별도 초기화 로직 활용
embedding_function = get_embedding_function()
vectorstore = get_vectorstore()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    full_text = extract_text_from_pdf(content)
    docs = split_text_into_chunks(full_text)
    vectorstore.add_documents(docs)
    return {"status": "success", "num_chunks": len(docs)}
