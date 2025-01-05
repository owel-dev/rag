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
          # 텍스트 파일 경로 생성
        text_path = os.path.join(save_dir, f"{base_filename}_{page_index}.txt")

          # 기존 파일이 존재하면 파일 내용을 읽어 사용
        if os.path.exists(text_path):
            with open(text_path, "r", encoding="utf-8") as text_file:
                page_text = text_file.read()
        else:
            # 페이지를 Pixmap으로 변환 (이미지화)
            page = doc[page_index]
            pix = page.get_pixmap(dpi=settings.OCR_ENGINE_DPI)

            # PIL Image로 변환
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            content = buffer.getvalue()

            # OCR 처리
            page_text = ocr_engine.do_ocr(content)

            # 텍스트 파일 저장
            with open(text_path, "w", encoding="utf-8") as text_file:
                text_file.write(page_text)

        all_texts.append(page_text)

    # 모든 페이지의 텍스트를 합쳐 반환
    return "\n".join(all_texts)
