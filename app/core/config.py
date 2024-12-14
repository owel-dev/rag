import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")
    UVICORN_PORT = int(os.getenv("UVICORN_PORT", 8080))

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GCP_API_KEY = os.getenv("GCP_API_KEY")

    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

    OCR_ENGINE = os.getenv("OCR_ENGINE", "easy-ocr")
    OCR_ENGINE_DPI = int(os.getenv("OCR_ENGINE_DPI", 70))
    PDF_IMAGE_SAVE_DIR = os.getenv("PDF_IMAGE_SAVE_DIR", "pdf-images")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
