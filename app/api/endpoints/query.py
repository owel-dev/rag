from fastapi import APIRouter
from app.models.request import QueryRequest
from app.services.llm_chain import get_qa_chain
from app.services.embeddings import get_embedding_function
from app.services.vectorstore import get_vectorstore

router = APIRouter()

embedding_function = get_embedding_function()
vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
qa_chain = get_qa_chain(retriever)


@router.post("/query")
async def query(request: QueryRequest):
    answer = qa_chain.run(request.query)
    return {"answer": answer}
