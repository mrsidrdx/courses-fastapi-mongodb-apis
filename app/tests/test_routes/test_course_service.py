from typing import List
from httpx import AsyncClient
import pytest

@pytest.mark.anyio
async def test_get_available_courses_success(client: AsyncClient):
    response = await client.get("/v1/courses")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_available_courses_return_type(client: AsyncClient):
    response = await client.get("/v1/courses")
    assert isinstance(response.json(), List)

@pytest.mark.anyio
async def test_get_available_courses_with_domain(client: AsyncClient):
    response = await client.get("/v1/courses?domain=science")
    assert response.json() == []

@pytest.mark.anyio
async def test_get_course_by_id_not_found(client: AsyncClient):
    response = await client.get("/v1/courses/26c41ef5-0844-4bea-b787-23951d475a4c")
    assert response.status_code == 500
    assert response.json()['errors'] == "Course not found"

@pytest.mark.anyio
async def test_get_course_by_id_invalid_uuid(client: AsyncClient):
    response = await client.get("/v1/courses/322523532523")
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "value is not a valid uuid"