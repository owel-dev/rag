import fitz  # PyMuPDF
import io
from PIL import Image
import os

from app.core import settings
from app.dependencies import IOCR


def extract_text_from_pdf(pdf_bytes: bytes,
                          ocr_engine: IOCR,
                          filename: str) -> str:
    # pdf_bytes를 직접 메모리 스트림으로 오픈
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # base filename (확장자 제거)
    base_filename = os.path.splitext(filename)[0]
    # 이미지 저장 디렉토리가 환경변수에서 지정되었다면 생성
    save_dir = settings.OCR_TEXT_SAVE_DIR
    if save_dir:
        # save_dir 아래에 파일명을 디렉토리로 생성
        save_dir = os.path.join(save_dir, base_filename)
        os.makedirs(save_dir, exist_ok=True)

    all_texts = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        # 페이지를 Pixmap으로 변환 (이미지화)
        pix = page.get_pixmap(dpi=settings.OCR_ENGINE_DPI)

        # PIL Image로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        content = buffer.getvalue()

        page_text = ocr_engine.do_ocr(content)

        if save_dir:
            text_path = os.path.join(save_dir, f"{base_filename}_{page_index}.txt")
            with open(text_path, "w", encoding="utf-8") as text_file:
                text_file.write(page_text)

        # 텍스트 클리닝 및 수집
        cleaned_text = page_text.replace("\n", " ")
        all_texts.append(cleaned_text)

    # 모든 페이지의 텍스트를 합쳐 반환
    return "\n\n".join(all_texts)
