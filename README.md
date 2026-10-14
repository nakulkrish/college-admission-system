# College Admission System

A FastAPI backend with PostgreSQL for managing student registrations, course catalogs, applications, document uploads, and admin workflows.

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost/college_admission
export APP_ENV=development
```

## Run
```bash
uvicorn app.main:app --reload
```

## Test
```bash
pytest -q
```

API docs are available at `http://localhost:8000/docs`.  
