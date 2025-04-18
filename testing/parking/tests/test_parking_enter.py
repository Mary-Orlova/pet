import pytest


@pytest.mark.parking
def test_parking_enter(client, test_client, test_parking):
    """Тест заезд на парковку"""
    response = client.post(
        "/client_parkings",
        json={"client_id": test_client.id, "parking_id": test_parking.id},
    )
    assert response.status_code == 200
    assert test_parking.count_available_places == 9
