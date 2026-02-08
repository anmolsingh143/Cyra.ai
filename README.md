# Cyra.ai

## Run locally

### Frontend
From the repo root:

```bash
cd frontend
npm install
npm run dev
```

The `frontend/` directory is a workspace root that delegates commands to the Next.js app in `frontend/frontend`.

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
