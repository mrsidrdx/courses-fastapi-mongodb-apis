from typing import List, Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class Chapter(BaseModel):
    """
    This is the description of the chapter model
    """
    id: UUID = Field(default_factory=uuid4, title="Chapter ID", description="The ID of the chapter.")
    name: str = Field(..., title="Chapter Name", description="The name of the chapter.")
    text: str = Field(..., title="Chapter Text", description="The text of the chapter.")
    ratings: Optional[List[int]] = []
    avg_rating: Optional[float] = 1

    class Config:
        title = 'Chapter'

class ChaptersView(BaseModel):
    chapters: List[Chapter]

    class Settings:
        projection = {"chapters": "$chapters"}

class ChapterRating(BaseModel):
    chapter_id: UUID = Field(..., title="Chapter ID", description="The ID of the chapter.")
    rating: int = Field(..., ge=0, le=1, title="Chapter Rating", description="The rating for the chapter (0: negative, 1: positive).")

    @validator('rating')
    def validate_rating(cls, value):
        if value not in [0, 1]:
            raise ValueError('Rating must be either 0 or 1.')
        return value

    class Config:
        title = 'ChapterRating'