from parking_app.models import Client, Parking


def test_exit_without_credit_card(client, db_session):
    """Тест клиент без карты"""
    client_no_card = Client(name="NoCard", surname="Test", car_number="A111AA")
    parking = Parking(
        address="ул. Без карты", opened=True, count_places=2, count_available_places=2
    )
    db_session.add_all([client_no_card, parking])
    db_session.commit()

    # Заезд
    client.post(
        "/client_parkings",
        json={"client_id": client_no_card.id, "parking_id": parking.id},
    )

    # Выезд
    response = client.delete(
        "/client_parkings",
        json={"client_id": client_no_card.id, "parking_id": parking.id},
    )
    assert response.status_code == 400
