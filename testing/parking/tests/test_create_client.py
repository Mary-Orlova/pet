def test_create_client(client):
    """Тест создания клиента"""
    response = client.post(
        "/clients",
        json={
            "name": "Иван",
            "surname": "Иванов",
            "credit_card": "4111111111111111",
            "car_number": "A123BC",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json
