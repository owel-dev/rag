import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import easyocr

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    # EasyOCR Reader 초기화 (여기서는 영어 'en'을 예로 사용)
    reader = easyocr.Reader(['ko'])

    # pdf_bytes를 직접 메모리 스트림으로 오픈
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    all_texts = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        # 페이지를 Pixmap으로 변환 (이미지화)
        pix = page.get_pixmap()
        # PIL Image로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        # numpy array로 변환
        page_np = np.array(img)

        # OCR 수행
        results = reader.readtext(page_np, detail=0)
        # 결과 리스트를 줄단위로 합치기
        page_text = "\n".join(results)
        all_texts.append(page_text)

    # 모든 페이지의 텍스트를 합쳐 반환
    return "\n\n".join(all_texts)
