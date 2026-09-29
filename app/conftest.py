import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app, tasks, Task, next_id


@pytest_asyncio.fixture
async def client():
    # очищаем хранилище перед каждым тестом
    tasks.clear()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c


@pytest_asyncio.fixture
async def sample_task(client):

    response = await client.post(
        "/create-task",
         json={"title": "test task", "description": "test description"})
    
    assert response.status_code == 200
    return response.json()["id"]
