from enum import Enum
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID

from pydantic import ValidationError
from server.models.course import Course, CourseRating
from beanie.operators import In
from bson import Binary

router = APIRouter()


class CourseSortingMode(str, Enum):
    ALPHABETICAL = "alphabetical"
    DATE = "date"
    RATING = "rating"


@router.get("/", summary="Get Available Courses", response_model=List[Course],
            response_description="List of Courses", description='''
                Endpoint to get a list of all available courses. This endpoint needs to support 3 modes of
                sorting: Alphabetical (based on course title, ascending), date (descending) and total course
                rating (descending). Additionaly, this endpoint needs to support optional filtering of courses
                based on domain
            ''')
async def get_available_courses(sort_by: CourseSortingMode = CourseSortingMode.ALPHABETICAL, domain: Optional[str] = Query(None)) -> List[Course]:
    # Retrieve courses
    try:
        # Apply optional filtering by domain
        if domain:
            courses = Course.find(In(Course.domain, [domain]))
        else:
            courses = Course.find({})

        # Sort courses based on the selected sort option
        if sort_by == CourseSortingMode.ALPHABETICAL:
            courses = courses.sort("+name")
        elif sort_by == CourseSortingMode.DATE:
            courses = courses.sort("-date")
        elif sort_by == CourseSortingMode.RATING:
            courses = courses.sort("-rating")

        # Aggregate all ratings from chapters and add average of them as rating
        pipeline = [
            {
                "$project": {
                    "rating": {
                        "$round": [{"$avg": "$chapters.avg_rating"}, 2]
                    },
                    "name": 1,
                    "date": 1,
                    "description": 1,
                    "domain": 1,
                    "chapters": 1
                }
            },
            {
                "$set": {
                    "rating": {"$ifNull": ["$rating", 0]}
                }
            },
            {
                "$replaceRoot": {"newRoot": "$$ROOT"}
            }
        ]

        courses = await courses.aggregate(aggregation_pipeline=pipeline, projection_model=Course).to_list()
        return courses

    except ValidationError as e:
        raise ValueError(e.errors())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{course_id}", summary="Get Course by ID", response_model=Course,
            response_description="Course Details", description='''
             Endpoint to get the course overview.
            ''')
async def get_course_by_id(course_id: UUID) -> Course:
    try:
        # Retrieve the course by ID
        course = await Course.get(course_id)

        if not course:
            raise ValueError("Course not found")

        binary_course_id = Binary.from_uuid(course_id)

        # Calculate the average rating of all chapters using MongoDB's aggregation
        pipeline = [
            {"$match": {"_id": binary_course_id}},
            {"$unwind": "$chapters"},
            {"$group": {"_id": str(course_id), "rating": {
                "$avg": "$chapters.avg_rating"}}}
        ]

        result = await Course.aggregate(aggregation_pipeline=pipeline, projection_model=CourseRating).to_list()

        if result:
            avg_rating = result[0].rating
        else:
            avg_rating = 0

        # Update the rating property of the course
        course.rating = round(avg_rating, 2)

        return course

    except ValidationError as e:
        raise ValueError(e.errors())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
