import logging

from app.core.config import settings
from app.core.logging import setup_logging

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

import asyncio
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=200)


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=200)
    done: bool | None = None


tasks: dict[int, Task] = {}
next_id = 1



@app.get("/health")
async def health_check():
    logger.debug("health check details: status=ok")
    logger.info("health check called")
    return {"status": "ok"}


@app.get('/tasks', response_model=list[Task])
async def get_tasks(done_only : bool = False):
    if done_only == True:
        return [task for task in tasks.values() if task.done]
    return list(tasks.values())


@app.get('/task/{task_id}', response_model=Task)
async def get_tasks(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='task not found')
    return task


@app.post('/create-task', response_model=Task)
async def create_task(payload: TaskCreate):
    if len(tasks) > 100:
        raise HTTPExeption(
            status_code=status.HTTP_409_CONFLICT,
            detail="Достигнут лимит задач",
        )
    global next_id
    task = Task(
        id=next_id,
        title=payload.title,
        description=payload.description,
        done=False
    )

    tasks[next_id] = task
    next_id += 1
    return task


@app.patch('/task/{task_id}', response_model=Task)
async def task_update(task_id: int, payload: TaskUpdate):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    updated_task = task.model_copy(
        update={k: v for k, v in payload.model_dump().items() if v is not None})
    tasks[task_id] = updated_task
    return updated_task


@app.delete('/task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    del tasks[task_id]
    return None


@app.get('/slow')
async def slow_endpoint():
    await asyncio.sleep(10)
    return {'message': 'Done'}

@app.get('/version')
async def version_endpoint() -> dict[str, str]:
    return {'version': settings.app_version}