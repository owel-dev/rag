from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(full_text: str, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.create_documents([full_text])
    return docs