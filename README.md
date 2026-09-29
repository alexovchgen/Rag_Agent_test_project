# task-api

CRUD-сервис для управления задачами. FastAPI + Docker + автодеплоцй.

## Локальный запуск

    conda create -y -n task-api python=3.11
    conda activate task-api
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Документация: http://localhost:8000/docs