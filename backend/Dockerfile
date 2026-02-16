FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY . ./backend

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 \
    fastapi pydantic pydantic-settings pymupdf python-multipart \
    qdrant-client uvicorn && \
    pip install --default-timeout=1000 \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --default-timeout=1000 transformers

# Create upload directory
RUN mkdir -p data/uploads

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
