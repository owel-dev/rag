FROM python:3.10-slim

WORKDIR /rag

COPY requirements.txt .

# pip 업그레이드 및 패키지 설치
RUN python3 -m pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]
