# Setup Instructions

## Local Development Setup

### step 1:
```bash
 Install uv
 ```

### Step 2: Clone the Repository
```bash
git clone https://github.com/your-username/mlops_final_project.git
cd mlops_final_project 
```

### Step3:  Create Virtual Environment & Install Dependencies.
``` bash 
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Step4: Start the Backend
```bash 
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### step5:start frontend
```bash 
source .venv/bin/activate  # Activate virtual environment
cd frontend
streamlit run app.py
```

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/mlops_final_project.git
cd mlops_final_project

# Start all services
docker compose up --build
```

### Access the Application
- Frontend UI: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

### Docker Commands

Start services:
```bash
docker compose up
```

Start in detached mode:
```bash
docker compose up -d
```

Rebuild and start:
```bash
docker compose up --build
```

Stop services:
```bash
docker compose down
```

Stop and remove volumes (clears database):
```bash
docker compose down -v
```

View logs:
```bash
docker compose logs
docker compose logs backend
docker compose logs frontend
docker compose logs qdrant
```

### Architecture
- **Qdrant**: Vector database for document embeddings
- **Backend**: FastAPI service with RAG pipeline
- **Frontend**: Streamlit UI for document upload and chat

All services run in isolated Docker containers connected via a bridge network.