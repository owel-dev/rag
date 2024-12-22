
### 프로젝트 디렉토리 구조

```bash
rag/
├── app                       # FastAPI 애플리케이션 소스 폴더
│   ├── core                  # 프로젝트 전역 설정, 구성 파일
│   │   ├── config.py         # 환경 변수, 설정값 정의
│   │   ├── __init__.py
│   ├── dependencies          # 의존성(재사용 가능 코드) 관리
│   │   ├── __init__.py       
│   │   ├── ocr.py            # OCR 관련 함수, 클래스
│   │   └── vectorstore.py    # 벡터 스토어 관련 함수, 클래스
│   ├── main.py               # FastAPI 진입점(엔트리 포인트)
│   ├── router                # 라우터(엔드포인트) 정의
│   │   ├── endpoints.py      # API 경로 및 핸들러 함수
│   │   ├── __init__.py
│   ├── schemas               # Pydantic 모델 등 스키마 정의
│   │   ├── __init__.py
│   │   └── request.py        # 요청/응답 데이터 모델
│   ├── services              # 서비스 레이어(실제 비즈니스 로직)
│   │   ├── __init__.py
│   │   ├── llm_chain.py      # LLM 관련 로직
│   │   ├── ocr.py            # OCR 로직
│   │   ├── text_preprocessing.py  # 텍스트 전처리 함수
│   │   └── vectorstore.py         # 벡터 변환, 저장, 유사도 검색 로직
│   └── test.py               # 테스트 스크립트(샘플 등)
├── docker-compose.yml         # Docker Compose 설정 파일 (Chroma, fastapi)
├── Dockerfile                 # Docker 이미지 빌드용 파일      
├── README.md                  # 프로젝트 개요 및 문서
└── requirements.txt           # Python 패키지 의존성 목록
```