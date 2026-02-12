import sys
from pathlib import Path
import pytest
from httpx import AsyncClient, ASGITransport


from hw1.main import app
from hw1.database import engine, Base

@pytest.fixture(autouse=True)
async def setup_database():
    """Создаем таблицы перед каждым тестом"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    """Клиент для тестов - уже открытый"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac  # Здесь client уже открыт, не нужно открывать в тесте