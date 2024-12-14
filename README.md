```bash
fastapi/
  ├─ app/
  │   ├─ main.py                    # FastAPI 진입점: app 인스턴스 생성 및 라우트 등록
  │   ├─ core/
  │   │   ├─ config.py              # 설정 관련 파일: 환경변수 로드, API 키, 경로 설정
  │   │   └─ __init__.py
  │   ├─ apis/
  │   │   ├─ endpoints/
  │   │   │   ├─ upload.py          # /upload 엔드포인트 라우트: PDF 업로드 -> OCR -> 벡터 스토어 인덱싱
  │   │   │   └─ query.py           # /query 엔드포인트 라우트: 사용자의 질의 -> RAG 파이프라인 -> 답변 반환
  │   │   └─ __init__.py
  │   ├─ services/
  │   │   ├─ ocr.py                 # OCR 관련 로직: PDF -> 이미지 변환 -> Tesseract OCR -> 텍스트 추출
  │   │   ├─ embeddings.py          # 임베딩 로직: OpenAI/HuggingFace Embeddings 초기화 및 제공
  │   │   ├─ vectorstore.py         # 벡터 스토어 초기화 및 관리: Chroma 인덱스 생성/문서 추가/조회
  │   │   ├─ llm_chain.py           # LLM 체인 설정: RetrievalQA 체인 생성, LLM/Retriever 연결
  │   │   └─ __init__.py
  │   ├─ models/
  │   │   ├─ request.py             # Pydantic 모델 정의: QueryRequest 등 요청 바디 모델
  │   │   └─ __init__.py
  │   ├─ utils/
  │   │   ├─ text_preprocessing.py  # 텍스트 전처리/스플릿팅 유틸: 긴 텍스트를 chunk로 분리
  │   │   └─ __init__.py
  │   └─ __init__.py
  ├─ requirements.txt               # Python 의존성 리스트
  ├─ Dockerfile                     # Docker 이미지를 위한 빌드 스크립트
  └─ ... (기타 CI/CD, 테스트 코드 등)
```