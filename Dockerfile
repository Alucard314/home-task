# Imagine de bază
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază requirements și instalează dependințele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază codul aplicației
COPY ./app ./app

COPY axiomatic-skill-458008-j5-6ccd088d7a48.json /creds/key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/creds/key.json

# Expune portul default FastAPI
EXPOSE 8080

# Rulează aplicația cu Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]