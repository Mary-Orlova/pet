import pytest
from parking_app.factories import ClientFactory, ParkingFactory
from parking_app.models import Client, ClientParking, Parking


def test_client_creation_with_factory(db_session):
    """Тест создания клиента через фабрику"""
    # Создаем клиента и проверяем базовые атрибуты
    client = ClientFactory()
    db_session.commit()

    # Проверка записи в БД
    assert client.id is not None
    assert db_session.query(Client).count() == 1

    # Проверка типов данных
    assert isinstance(client.name, str)
    assert isinstance(client.surname, str)
    assert client.credit_card is None or isinstance(client.credit_card, str)
    assert len(client.car_number) == 6  # "A123BC"


def test_parking_creation_with_factory(db_session):
    """Тест создания парковки через фабрику"""
    # Явное задание количества мест (проверка LazyAttribute)
    parking = ParkingFactory(count_places=20)
    db_session.commit()

    # Проверка записи в БД
    assert parking.id is not None
    assert db_session.query(Parking).count() == 1

    # Проверка зависимых полей
    assert parking.count_available_places == 20
    assert isinstance(parking.address, str)
    assert isinstance(parking.opened, bool)


def test_no_credit_card(client, db_session):
    """Тест клиента без карты (с проверкой API)"""
    client_no_card = ClientFactory(credit_card=None)
    parking = ParkingFactory(count_places=5)
    db_session.commit()

    # Заезд
    client.post(
        "/client_parkings",
        json={"client_id": client_no_card.id, "parking_id": parking.id},
    )

    # Выезд (должен вернуть ошибку 400)
    response = client.delete(
        "/client_parkings",
        json={"client_id": client_no_card.id, "parking_id": parking.id},
    )
    assert response.status_code == 400
    assert b"No credit card linked" in response.data  # Сравнение с байтовой строкой


# Дубликаты тестов из задания 3 с использованием фабрик
def test_original_client_creation(client):
    """Дубликат теста создания клиента API"""
    client_data = ClientFactory.build()
    response = client.post(
        "/clients",
        json={
            "name": client_data.name,
            "surname": client_data.surname,
            "credit_card": client_data.credit_card,
            "car_number": client_data.car_number,
        },
    )
    assert response.status_code == 201
    assert "id" in response.json


def test_original_parking_creation(client):
    """Дубликат теста создания парковки API"""
    parking_data = ParkingFactory.build(count_places=15)
    response = client.post(
        "/parkings",
        json={
            "address": parking_data.address,
            "opened": parking_data.opened,
            "count_places": parking_data.count_places,
        },
    )
    assert response.status_code == 201
    assert "id" in response.json
