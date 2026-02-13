FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./
COPY frontend ./frontend

# Install dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Expose the port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
