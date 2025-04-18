from datetime import datetime

import pytest
from parking_app.app import create_app
from parking_app.database import db as _db
from parking_app.models import Client, ClientParking, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["SQLALCHEMY_ECHO"] = True
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        yield _app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def second_client(db_session):
    client = Client(
        name="Second",
        surname="Client",
        credit_card="2222222222222222",
        car_number="B456CD",
    )
    db_session.add(client)
    db_session.commit()
    return client


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield _db.session


@pytest.fixture
def test_client(db_session):
    """Тест клиента"""
    client = Client(
        name="Test", surname="User", credit_card="1111111111111111", car_number="A123BC"
    )
    db_session.add(client)
    db_session.commit()
    return client


@pytest.fixture
def test_parking(db_session):
    """Тест паркинга"""
    parking = Parking(
        address="ул. Тест, 1", opened=True, count_places=10, count_available_places=10
    )
    db_session.add(parking)
    db_session.commit()
    return parking


@pytest.fixture
def test_log(db_session, test_client, test_parking):
    """Тест лога"""
    log = ClientParking(
        client_id=test_client.id,
        parking_id=test_parking.id,
        time_in=datetime(2025, 1, 1, 10, 0),
    )
    db_session.add(log)
    db_session.commit()
    return log
