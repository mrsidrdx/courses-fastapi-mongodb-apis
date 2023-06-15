import json
import asyncio
import sys
import os

from pydantic import ValidationError

# Get path for courses.json
current_file_path = os.path.dirname(os.path.abspath(__file__))
courses_json_path = os.path.join(current_file_path, "courses.json")

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.server.database import DatabaseClient
from app.server.models.course import Course

class CourseParser:

    async def db_init(self):
        await DatabaseClient.init_db()

    def parse_json_to_object(self):
        # Read the courses.json file
        with open(courses_json_path, "r") as file:
            courses_data = json.load(file)

        # Validate and convert the data to Course objects
        courses = []
        for course_data in courses_data:
            try:
                course = Course(**course_data)
            except ValidationError as e:
                raise ValueError(e.errors())
            courses.append(course)

        return courses

    async def upload_course_documents(self):
        await self.db_init()
        await Course.find({}).delete()
        courses = self.parse_json_to_object()
        # Insert course documents into courses collection
        await Course.insert_many(courses)

if __name__ == "__main__":
    courses_obj = CourseParser()

    # Create an event loop
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    try:
        # Run the async function in the event loop
        loop.run_until_complete(courses_obj.upload_course_documents())

        # Close the event loop
        loop.close()
    except KeyboardInterrupt:
        pass
