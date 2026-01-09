# RAG 시스템

FastAPI, LangChain, OpenAI, Chroma를 활용한 문서 기반 질의응답(RAG) 시스템입니다.

PDF 문서를 업로드하면 OCR로 텍스트를 추출하고, 벡터 데이터베이스에 저장하여 자연어 질의를 통해 관련 정보를 검색하고 답변을 생성합니다.

## 주요 기능

- PDF 문서 텍스트 추출 (OCR 지원: EasyOCR, GCP Vision API, Tesseract)
- 문서 청크 분할 및 벡터 임베딩 저장
- 의미 기반 유사도 검색
- LLM 기반 질의응답 (OpenAI GPT 모델)
- 토큰 기반 인증 (선택 사항)
- Docker 기반 간편한 배포

## 기술 스택

- **Backend Framework**: FastAPI
- **LLM Framework**: LangChain
- **Vector Database**: Chroma
- **Embedding Models**: HuggingFace (sentence-transformers), OpenAI
- **LLM**: OpenAI GPT (gpt-4o-mini, gpt-4 등)
- **OCR Engines**: EasyOCR, Google Cloud Vision API, Tesseract
- **Containerization**: Docker, Docker Compose

## 요구사항

- Docker
- Docker Compose
- OpenAI API Key (필수)
- Google Cloud Vision API Key (선택, 한글 PDF OCR 시 권장)

## 설치 및 실행

### 1. 환경 변수 설정

.env.example 파일을 참고하여 프로젝트 루트에 .env 파일을 생성하고 아래 내용을 채워줍니다.

```bash
# 서버 설정
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8080

# API Keys
OPENAI_API_KEY=your-openai-api-key  # 필수
GCP_API_KEY=your-gcp-api-key        # OCR_ENGINE=gcp-vision 사용 시 필수

# Vector Store 설정
VECTORSTORE_HOST=chroma
VECTORSTORE_PORT=8000
VECTORSTORE_EMBED_PROVIDER=hugging-face  # hugging-face 또는 openai
VECTORSTORE_EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2

# OCR 설정
OCR_ENGINE=easy-ocr  # easy-ocr, gcp-vision, tesseract 중 선택
OCR_ENGINE_DPI=70
PDF_IMAGE_SAVE_DIR=pdf_images

# LLM 모델 선택
LLM_MODEL=gpt-4o-mini  # gpt-4o-mini, gpt-4, gpt-3.5-turbo 등
```

**환경 변수 설명:**
- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `GCP_API_KEY`: Google Cloud Vision API 키 (한글 PDF 처리 시 권장)
- `OCR_ENGINE`: OCR 엔진 선택
  - `easy-ocr`: 다국어 지원, GPU 권장
  - `gcp-vision`: 한글 문서 인식 정확도 높음 (API 키 필요)
  - `tesseract`: 무료, 영문 중심
- `VECTORSTORE_EMBED_PROVIDER`: 임베딩 모델 제공자
- `LLM_MODEL`: 사용할 OpenAI 모델명

### 2. 토큰 인증 설정 (선택 사항)

API 접근을 제한하려면 token_whitelist.yaml 파일을 생성합니다.

```bash
cp token_whitelist.yaml.example token_whitelist.yaml
```

token_whitelist.yaml 파일에 허용할 토큰 목록을 추가합니다.

### 3. Docker 컨테이너 실행

```bash
docker compose up -d
```

컨테이너가 시작되면 약 20초 후 FastAPI 서버가 준비됩니다.

## API 사용법

### 1. PDF 문서 업로드

PDF 파일을 업로드하여 벡터 데이터베이스에 저장합니다.

**요청:**
```bash
curl -X POST "http://localhost:8080/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-document.pdf"
```

**응답 예시:**
```json
{
  "status": "success",
  "num_chunks": 42
}
```

### 2. 문서 기반 질의

업로드된 문서 내용을 기반으로 질문에 대한 답변을 받습니다.

**요청:**
```bash
curl -X POST "http://localhost:8080/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "문서의 주요 내용은 무엇인가요?"}'
```

**응답 예시:**
```json
{
  "answer": "문서의 주요 내용은..."
}
```

### 토큰 인증 사용 시

token_whitelist.yaml 파일을 설정한 경우, 요청 시 Authorization 헤더에 토큰을 포함해야 합니다.

```bash
curl -X POST "http://localhost:8080/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"query": "질문 내용"}'
```


## 프로젝트 디렉토리 구조

```bash
rag/
├── app/                              # FastAPI 애플리케이션 소스 폴더
│   ├── core/                         # 프로젝트 전역 설정
│   │   ├── config.py                 # 환경 변수, 설정값 정의
│   │   └── __init__.py
│   ├── dependencies/                 # 의존성 주입 및 재사용 가능 코드
│   │   ├── ocr.py                    # OCR 엔진 팩토리
│   │   ├── vectorstore.py            # 벡터 스토어 인스턴스 제공
│   │   └── __init__.py
│   ├── middleware/                   # 미들웨어
│   │   ├── auth_middleware.py        # 토큰 인증 미들웨어
│   │   └── __init__.py
│   ├── router/                       # API 라우터
│   │   ├── endpoints.py              # API 엔드포인트 정의 (/upload, /query)
│   │   └── __init__.py
│   ├── schemas/                      # Pydantic 스키마
│   │   ├── request.py                # 요청 데이터 모델
│   │   └── __init__.py
│   ├── services/                     # 비즈니스 로직
│   │   ├── llm_chain.py              # LangChain QA 체인 구성
│   │   ├── ocr.py                    # PDF 텍스트 추출
│   │   ├── text_preprocessing.py     # 텍스트 청크 분할
│   │   ├── vectorstore.py            # 벡터 임베딩 및 저장
│   │   └── __init__.py
│   └── main.py                       # FastAPI 애플리케이션 진입점
├── .dockerignore                     # Docker 빌드 제외 파일
├── .env.example                      # 환경 변수 템플릿
├── .gitignore                        # Git 제외 파일
├── docker-compose.yml                # Docker Compose 설정 (RAG, Chroma)
├── Dockerfile                        # Docker 이미지 빌드 파일
├── README.md                         # 프로젝트 문서
├── requirements.txt                  # Python 패키지 의존성
└── token_whitelist.yaml.example      # 인증 토큰 화이트리스트 템플릿
```

## 아키텍처

1. **문서 업로드 플로우**
   - PDF 업로드 → OCR 텍스트 추출 → 텍스트 청크 분할 → 벡터 임베딩 → Chroma 저장

2. **질의응답 플로우**
   - 사용자 질의 → 벡터 유사도 검색 → 관련 문서 청크 검색 → LLM 컨텍스트 생성 → 답변 생성

## 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여

이슈 및 풀 리퀘스트는 언제나 환영합니다!

## 문의

프로젝트 관련 문의사항이나 버그 리포트는 GitHub Issues 를 통해 제출해주세요.
