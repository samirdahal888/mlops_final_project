FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt && \
    pip install --default-timeout=1000 --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY . ./backend

# Create upload directory
RUN mkdir -p data/uploads

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
