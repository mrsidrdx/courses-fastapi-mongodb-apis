from beanie import init_beanie
import motor.motor_asyncio

from .models.course import Course
from .config import settings

class DatabaseClient:
    @staticmethod
    async def init_db():
        client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.DATABASE_URL
        )
        await init_beanie(database=client.course_db, document_models=[Course])
