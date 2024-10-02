import pytest
from fastapi import status


@pytest.mark.api
@pytest.mark.integration
async def test_get_all_cats(test_client, cat_payload, breed_payload):
    """Тест взятия всех кошачих из БД."""
    response = await test_client.post("/api/cats")
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json["cats"][0]["color"] == cat_payload["color"]
    assert response_json["cats"][0]["breed"]["name"] == breed_payload["name"]
    assert response_json["cats"][0]["age_in_months"] == cat_payload["age_in_months"]
    assert response_json["cats"][0]["description"] == cat_payload["description"]


@pytest.mark.api
@pytest.mark.integration
async def test_get_all_breeds(test_client, breed_payload):
    """Тест взятия всех пород из БД."""
    response = await test_client.post("/api/cats/breeds")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["breeds"][0]["name"] == breed_payload["name"]


@pytest.mark.api
@pytest.mark.integration
async def test_get_cats_with_breed(test_client, breed_payload, breed_name):
    """Тест взятия всех котов определенной породы из БД."""
    response = await test_client.post(f"/api/cats/breeds/{breed_name}")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["cats"][0]["breed"]["name"] == breed_payload["name"]
