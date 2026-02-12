# Setup Instructions

## step 1:
```bash
 Install uv
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
uv pip install -e .
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