FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./
COPY backend ./backend

# Install dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Create data directory
RUN mkdir -p data/uploads

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
