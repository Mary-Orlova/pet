import factory
from faker import Faker

from .database import db
from .models import Client, Parking

fake = Faker("ru_RU")


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"  # Автокоммит

    name = factory.LazyFunction(lambda: fake.first_name())
    surname = factory.LazyFunction(lambda: fake.last_name())
    credit_card = factory.LazyAttribute(
        lambda _: fake.credit_card_number() if fake.boolean(70) else None
    )
    car_number = factory.LazyFunction(lambda: fake.bothify("?###??").upper())


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.LazyFunction(lambda: fake.address())
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=10, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
