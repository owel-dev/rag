from abc import ABC, abstractmethod
from functools import lru_cache

import easyocr
import pytesseract
from google.api_core.client_options import ClientOptions
from google.cloud import vision
from PIL import Image
import numpy as np
import io

from app.core import settings


class IOCR(ABC):
    @abstractmethod
    def do_ocr(self, content: bytes) -> str:
        pass


class GcpVisionOCR(IOCR):
    def __init__(self, api_key: str):
        client_options = ClientOptions(api_key=api_key)
        self.client = vision.ImageAnnotatorClient(client_options=client_options)

    def do_ocr(self, content: bytes) -> str:
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)

        texts = response.text_annotations
        if texts:
            return texts[0].description.strip()
        return ""


class EasyOCROCR(IOCR):
    def __init__(self, languages=['ko']):
        self.reader = easyocr.Reader(languages)

    def do_ocr(self, content: bytes) -> str:
        img = Image.open(io.BytesIO(content))
        page_np = np.array(img)
        results = self.reader.readtext(page_np, detail=0)
        if results:
            return "\n".join(results).strip()
        return ""


class TesseractOCR(IOCR):
    def __init__(self, lang: str = "kor"):
        self.lang = lang

    def do_ocr(self, content: bytes) -> str:
        img = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(img, lang=self.lang)
        return text.strip()


@lru_cache()
def get_gcp_vision_engine() -> IOCR:
    return GcpVisionOCR(api_key=settings.GCP_API_KEY)


@lru_cache()
def get_easy_ocr_engine() -> IOCR:
    return EasyOCROCR()


@lru_cache()
def get_tesseract_engine() -> IOCR:
    return TesseractOCR()


def get_ocr_engine() -> IOCR:
    match settings.OCR_ENGINE:
        case "gcp-vision":
            return get_gcp_vision_engine()
        case "easy-ocr":
            return get_easy_ocr_engine()
        case "tesseract":
            return get_tesseract_engine()
