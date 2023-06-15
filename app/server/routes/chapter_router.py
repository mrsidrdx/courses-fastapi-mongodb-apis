from uuid import UUID
from fastapi import APIRouter, HTTPException

from pydantic import ValidationError
from server.models.chapter import Chapter, ChaptersView, ChapterRating
from server.models.course import Course
from beanie.operators import ElemMatch, Set

router = APIRouter()


@router.get("/{chapter_id}", summary="Get Chapter by ID", response_model=Chapter,
            response_description="Chapter Details", description='''
            Endpoint to get specific chapter information.
            ''')
async def get_chapter_by_id(chapter_id: UUID) -> Chapter:
    try:
        chapters = await Course.find_one(ElemMatch(Course.chapters, {"id": chapter_id}), projection_model=ChaptersView)
        
        if not chapters:
            raise ValueError('Chapter not found.')
        
        for chapter in chapters.chapters:
            if chapter.id == chapter_id:
                return chapter

    except ValidationError as e:
        raise ValueError(e.errors())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/rating", summary="Rate Chapter",
            response_description="Rate Chapter", description='''
            Endpoint to allow users to rate each chapter (positive/negative), while aggregating all ratings
            for each course.
            ''')
async def post_chapter_rating(chapter_rating: ChapterRating) -> dict:
    try:
        chapters = await Course.find_one(ElemMatch(Course.chapters, {"id": chapter_rating.chapter_id}), projection_model=ChaptersView)
        
        if not chapters:
            raise ValueError('Chapter not found.')
        
        for chapter in chapters.chapters:
            if chapter.id == chapter_rating.chapter_id:
                chapter.ratings.append(chapter_rating.rating)
                chapter.avg_rating = round(sum(chapter.ratings) / len(chapter.ratings), 2)

        await Course.find_one(ElemMatch(Course.chapters, {"id": chapter_rating.chapter_id})).update(Set({Course.chapters: chapters.chapters}))

        return {
            'success': True
        }

    except ValidationError as e:
        raise ValueError(e.errors())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
