import os
import tempfile
import numpy as np
from pdf2image import convert_from_path
import easyocr


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    # EasyOCR Reader 초기화 (여기서는 영어 'en'을 예로 사용)
    reader = easyocr.Reader(['en'])

    # PDF 파일을 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    # PDF 각 페이지를 이미지로 변환
    pages = convert_from_path(tmp_path)
    os.remove(tmp_path)

    all_texts = []
    for page in pages:
        # PIL Image -> numpy array 변환
        page_np = np.array(page)

        # OCR 수행 (detail=0으로 설정하면 텍스트 부분만 리스트 형태로 반환)
        results = reader.readtext(page_np, detail=0)
        # 결과 리스트를 줄단위로 합치기
        page_text = "\n".join(results)
        all_texts.append(page_text)

    # 모든 페이지의 텍스트를 합쳐 반환
    return "\n\n".join(all_texts)
