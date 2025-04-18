import pytest
from parking_app.models import Client, ClientParking, Parking


@pytest.mark.parking
def test_parking_exit(client, test_client, test_parking, test_log):
    """Тест проверки, что карта привязана"""
    assert test_client.credit_card is not None
    response = client.delete(
        "/client_parkings",
        json={"client_id": test_client.id, "parking_id": test_parking.id},
    )
    assert response.status_code == 200
    assert test_parking.count_available_places == 10

    # Обновляем объект из БД
    updated_log = ClientParking.query.get(test_log.id)
    assert updated_log.time_out > updated_log.time_in
