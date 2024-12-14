import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHROMA_URL = os.getenv("CHROMA_URL")
    # CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_storage")
    # OCR 설정, PDF 처리 관련 config 등 추가 가능


settings = Settings()
