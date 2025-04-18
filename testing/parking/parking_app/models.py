from .database import db


class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))
    parkings = db.relationship("ClientParking", back_populates="client", lazy=True)


class Parking(db.Model):
    __tablename__ = "parking"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    clients = db.relationship("ClientParking", back_populates="parking", lazy=True)


class ClientParking(db.Model):
    __tablename__ = "client_parking"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship(
        "Client", back_populates="parkings"
    )  # через back_populates
    parking = db.relationship(
        "Parking", back_populates="clients"
    )  # через back_populates

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )
