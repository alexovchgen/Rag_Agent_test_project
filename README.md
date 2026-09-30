# task-api

CRUD-сервис для управления задачами. FastAPI + Docker + автодеплоцй.

## Локальный запуск

    conda create -y -n task-api python=3.11
    conda activate task-api
    pip install -r requirements.txt
    uvicorn app.main:app --reload


## Живой сервис

http://5-63-158-113.nip.io/docs