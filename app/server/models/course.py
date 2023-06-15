from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
import pymongo
from uuid import UUID, uuid4

from .chapter import Chapter


class Course(Document):
    """
    This is the description of the course model
    """
    id: UUID = Field(default_factory=uuid4, title="Course ID", description="The ID of the course.", alias="_id")
    name: str = Field(..., title="Course Name", description="The name of the course.")
    date: float = Field(..., title="Course Date", description="The date of the course.")
    description: str = Field(..., title="Course Description", description="A description of the course.")
    domain: List[str] = Field(..., title="Course Domain", description="The domain(s) of the course.")
    chapters: List[Chapter] = Field([], title="Course Chapters", description="The chapters of the course.")
    rating: Optional[float]

    class Settings:
        name = "courses"
        indexes = [
            pymongo.IndexModel(
                [("name", pymongo.ASCENDING)],
                name="name_string_index_ASCENDING",
            ),
            pymongo.IndexModel(
                [("date", pymongo.DESCENDING)],
                name="date_float_index_DESCENDING",
            ),
            pymongo.IndexModel(
                [("rating", pymongo.DESCENDING)],
                name="rating_float_index_DESCENDING",
            ),
        ]

    class Config:
        title = 'Course'
        schema_extra = {
            "example": {
                "name":"Highlights of Calculus",
                "date":1530133200,
                "description":"Highlights of Calculus is a series of short videos that introduces the basic ideas of calculus \u2014 how it works and why it is important. The intended audience is high school students, college students, or anyone who might need help understanding the subject.\nIn addition to the videos, there are summary slides and practice problems complete with an audio narration by Professor Strang. You can find these resources to the right of each video.",
                "domain":[
                    "mathematics"
                ],
                "chapters":[
                    {
                        "name":"Gil Strang's Introduction to Calculus for Highlights for High School",
                        "text":"Highlights of Calculus"
                    }
                ]
            }
        }

class CourseRating(BaseModel):
    _id: str
    rating: float