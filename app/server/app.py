from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .database import DatabaseClient
from .routes.course_router import router as CourseRouter
from .routes.chapter_router import router as ChapterRouter

app = FastAPI(title="Courses FastAPI Service")

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "errors": str(exc)},
    )

@app.exception_handler(HTTPException)
async def value_error_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong", "errors": exc.detail},
    )

@app.on_event("startup")
async def app_init():
    await DatabaseClient.init_db()
    app.include_router(CourseRouter, prefix="/v1/courses", tags=["Course Service"])
    app.include_router(ChapterRouter, prefix="/v1/chapters", tags=["Chapter Service"])