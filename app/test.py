from app.services import vectorstore

query = ""
results = vectorstore.similarity_search(query, k=4)  # k는 반환할 문서 수
for i, doc in enumerate(results):
    print(f"Document {i+1}:\n{doc.page_content}\n")