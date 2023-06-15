from httpx import AsyncClient
import pytest

@pytest.mark.anyio
async def test_get_chapter_by_id_failure(client: AsyncClient):
    response = await client.get("/v1/chapters/26c41ef5-0844-4bea-b787-23951d475a4c")
    assert response.status_code == 500
    assert response.json()['errors'] == "Chapter not found."

@pytest.mark.anyio
async def test_get_chapter_by_id_invalid_uuid(client: AsyncClient):
    response = await client.get("/v1/chapters/3542535235")
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "value is not a valid uuid"

@pytest.mark.anyio
async def test_post_chapter_rating_invalid_rating(client: AsyncClient):
    response = await client.post("/v1/chapters/rating", json={
        "chapter_id": "26c41ef5-0844-4bea-b787-23951d475a4c",
        "rating": 2
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value is less than or equal to 1"