FROM python:3.11-slim

WORKDIR /app

# Copy frontend files
COPY . ./frontend

# Install Python dependencies
RUN pip install --no-cache-dir streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0"]
