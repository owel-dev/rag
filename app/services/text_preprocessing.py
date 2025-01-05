import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_text_into_chunks(full_text: str,
                           act: str,
                           chunk_size=1000,
                           chunk_overlap=100):
    article_pattern = re.compile(r"제\s*\d+조\(")

    lines = full_text.splitlines()
    article_texts = []
    current_lines = []

    for line in lines:
        if article_pattern.search(line):
            # 새 '조' 헤더를 만나면, 이전까지의 라인 묶음을 하나의 조로 저장
            if current_lines:
                article_texts.append("\n".join(current_lines))
            current_lines = [line]
        else:
            current_lines.append(line)

    # 마지막 잔여분 처리
    if current_lines:
        article_texts.append("\n".join(current_lines))

    # 2. 각 조 내용이 너무 길면, RecursiveCharacterTextSplitter로 나눈다.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    docs = []

    for idx, article in enumerate(article_texts):
        # 2차 분할
        sub_docs = splitter.create_documents([article])
        for doc in sub_docs:
            metadata_dict = {
                "act": act,
                **doc.metadata
            }
            if idx != 0:
                metadata_dict["article"] = idx

            new_doc = Document(
                metadata=metadata_dict,
                page_content=doc.page_content
            )
            docs.append(new_doc)

    return docs
