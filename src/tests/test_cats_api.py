import pytest
from fastapi import status

from src.app.schemas import schemas


@pytest.mark.api
@pytest.mark.integration
async def test_get_all_cats(test_client, cat_payload, breed_payload):
    """Тест взятия всех кошачих из БД."""
    response = await test_client.get("/api/cats")
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
    response = await test_client.get("/api/cats/breeds")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["breeds"][0]["name"] == breed_payload["name"]


@pytest.mark.api
@pytest.mark.integration
async def test_get_cats_with_breed(
    test_client, cat_payload, breed_payload, breed_name,
):
    """Тест взятия всех котов определенной породы из БД."""
    response = await test_client.get(f"/api/cats/breeds/{breed_name}")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["cats"][0]["breed"]["name"] == breed_payload["name"]
    assert response_json["cats"][0]["color"] == cat_payload["color"]
    assert response_json["cats"][0]["age_in_months"] == cat_payload["age_in_months"]
    assert response_json["cats"][0]["description"] == cat_payload["description"]


@pytest.mark.api
@pytest.mark.integration
async def test_get_cats_with_id(test_client, cat_payload, breed_payload, cat_id):
    """Тест взятия по его id из БД."""
    response = await test_client.get(f"/api/cats/{cat_id}")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["id"] == cat_id
    assert response_json["color"] == cat_payload["color"]
    assert response_json["breed"]["name"] == breed_payload["name"]
    assert response_json["age_in_months"] == cat_payload["age_in_months"]


@pytest.mark.api
@pytest.mark.integration
async def test_create_cat(test_client, create_cat_payload):
    """Тест записи объекта Cat в БД."""
    response = await test_client.post("/api/cats", json=create_cat_payload)
    response_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["status"] == schemas.Status.success.value
    assert response_json["message"] == "Запись создана"


@pytest.mark.api
@pytest.mark.integration
async def test_delete_cat(test_client, cat_id):
    """Тест записи объекта Cat в БД."""
    response = await test_client.delete(f"/api/cats/{cat_id}")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["status"] == schemas.Status.success.value
    assert response_json["message"] == "Запись удалена"


@pytest.mark.api
@pytest.mark.integration
async def test_update_cat(test_client, cat_id, update_cat_payload):
    """Тест записи объекта Cat в БД."""
    response = await test_client.patch(
        f"/api/cats/{cat_id}", json=update_cat_payload,
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["status"] == schemas.Status.success.value
    assert response_json["message"] == "Запись обновлена"
