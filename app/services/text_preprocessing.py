import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_text_into_chunks(full_text: str, title: str, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.create_documents([full_text])

    title = os.path.splitext(title)[0]

    enriched_docs = [
        Document(
            metadata={"title": title, **doc.metadata},
            page_content=f"{title} : {doc.page_content}"
        )
        for doc in docs
    ]

    return enriched_docs
