# Imagine de bază
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază requirements și instalează dependințele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază codul aplicației
COPY ./app ./app

# Expune portul default FastAPI
EXPOSE 8080

# Rulează aplicația cu Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]