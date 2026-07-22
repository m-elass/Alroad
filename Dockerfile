# KNAVE — imagen para Render / Hugging Face / cualquier host Docker
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg libreoffice-writer libreoffice-impress libreoffice-calc \
        fonts-dejavu-core fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV KNAVE_SERVER=1
EXPOSE 8666
CMD ["python", "main.py"]
