import fitz  # PyMuPDF
import io
from PIL import Image
import os

from app.core import settings
from app.dependencies import IOCR


def extract_text_from_pdf(pdf_bytes: bytes,
                          ocr_engine: IOCR) -> str:
    # pdf_bytes를 직접 메모리 스트림으로 오픈
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # 이미지 저장 디렉토리가 환경변수에서 지정되었다면 생성
    save_dir = settings.PDF_IMAGE_SAVE_DIR
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    all_texts = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        # 페이지를 Pixmap으로 변환 (이미지화)
        pix = page.get_pixmap(dpi=settings.OCR_ENGINE_DPI)

        # PIL Image로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 이미지 파일로 저장 (옵션)
        if save_dir:
            img_path = os.path.join(save_dir, f"page_{page_index}.png")
            img.save(img_path, "PNG")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        content = buffer.getvalue()

        page_text = ocr_engine.do_ocr(content)
        all_texts.append(page_text)

    # 모든 페이지의 텍스트를 합쳐 반환
    return "\n\n".join(all_texts)
