# Setup Instructions

## step 1: Install uv
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
 ```

## Step 2: Clone the Repository
```bash
git clone https://github.com/your-username/mlops_final_project.git
cd mlops_final_project 
```

## Step3:  Create Virtual Environment & Install Dependencies.
``` bash 
uv venv
source .venv/bin/activate
uv sync
```
## Step 4: Start Qdrant container 
```bash
docker run -d \
  -p 6333:6333 \
  -v qdrant_data:/qdrant/storage \
  --name qdrant \
  qdrant/qdrant
```

## Step4: Start the Backend
```bash 
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### step5:start frontend
```bash 
source .venv/bin/activate  # Activate virtual environment
cd frontend
streamlit run app.py
```