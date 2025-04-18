import pytest


@pytest.mark.parametrize(
    "opened,places,expected_code",
    [
        (True, 0, 400),  # 0 мест → ошибка
        (True, 10, 201),
        (False, 5, 201),  # Создать можно, но заехать нельзя
    ],
)
def test_create_parking(client, opened, places, expected_code):
    """Тест создания паркинга"""
    response = client.post(
        "/parkings",
        json={
            "address": "ул. Параметризованная",
            "opened": opened,
            "count_places": places,
        },
    )
    assert response.status_code == expected_code
