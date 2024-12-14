FROM python:3.11-slim

# 패키지 목록 업데이트 및 필요한 패키지 설치
# build-essential: C/C++ 컴파일 툴체인 (Alpine의 build-base 대체)
# libsqlite3-dev: sqlite3 관련 개발 헤더 (Chroma 등이 필요)
# libffi-dev: 파이썬 패키지 빌드 필요할 수 있음
# libjpeg-dev, zlib1g-dev: Pillow, pdf2image 등 이미지 처리 패키지 빌드에 필요
# libfreetype6-dev, liblcms2-dev, libopenjp2-7-dev, libtiff5-dev: Pillow 빌드에 필요한 이미지 라이브러리
# tk-dev, tcl-dev: Pillow 등에서 필요할 수 있는 tk/tcl 지원
# curl: 필요시
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tk-dev \
    tcl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*



WORKDIR /app

# requirements.txt 먼저 복사
COPY requirements.txt .

# pip, setuptools, wheel 최신화 후 requirements 설치
RUN python3 -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install -U langchain-community && pip install python-multipart tiktoken

# 나머지 소스 코드 복사
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
