from httpx import AsyncClient
import pytest

import sys
import os

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.app import app
from server.routes.course_router import router as CourseRouter
from server.routes.chapter_router import router as ChapterRouter
from server.database import DatabaseClient

@pytest.fixture
async def db_connection():
    # Initialize the database
    await DatabaseClient.init_db()
    

@pytest.fixture
async def start_app(db_connection):
    app.include_router(CourseRouter, prefix="/v1/courses", tags=["Course Service"])
    app.include_router(ChapterRouter, prefix="/v1/chapters", tags=["Chapter Service"])

    # Return the FastAPI app
    yield app

@pytest.fixture
async def client(start_app):
    # Create a test client using the initialized app
    async with AsyncClient(app=start_app, base_url="http://test", follow_redirects=True) as client:
        yield client