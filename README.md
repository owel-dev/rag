FastAPI, Lagnchain, ChatGPT, Chroma 스펙으로 간단하게 구현한 RAG 시스템입니다.

### 사용법
1. .env.example 파일의 내용을 참고하여 .env 파일을 루트 경로에 생성합니다.
2. .env파일의 내용을 채워줍니다.  
    2 - 1. `GCP_API_KEY` 환경변수는 OCR_ENGINE 으로 gcp-vision을 사용하지 않는다면 필수는 아닙니다.  
    (한글 PDF 문서의 경우, OCR ENGINE 으로 GCP Vision API를 적극 추천합니다.)  
    2 - 2. `OPENAI_API_KEY` 환경변수와 `LLM_MODEL` 환경변수는 **필수로** 채워야 합니다.
3. `docker compose up -d` 명령을 실행합니다.
4. fastapi 컨테이너에서 python이 빌드된 후 (20초정도 걸림)
5. `http://localhost:8080/api/v1/upload` url에 multipart/form-data 요청에서 파일 필드 이름을 file로 지정하여 pdf파일을 업로드 요청을 보냅니다.
6. `http://localhost:8080/api/v1/query` url에  아래와 같은 요청을 보냅니다.
    ```json
    {"query": "LLM에 질문할 내용"}
    ```


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