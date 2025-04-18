from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .database import db
from .models import Client, ClientParking, Parking

api = Blueprint("api", __name__, url_prefix="/")  # Префикс маршрута


# клиенты и парковки


@api.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return (
        jsonify([{"id": c.id, "name": c.name, "surname": c.surname} for c in clients]),
        200,
    )


@api.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return (
        jsonify(
            {
                "id": client.id,
                "car_number": client.car_number,
                "credit_card": client.credit_card,
            }
        ),
        200,
    )


@api.route("/clients", methods=["POST"])
def create_client():
    data = request.json
    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id}), 201


@api.route("/parkings", methods=["POST"])
def create_parking():
    data = request.json

    # Валидация количества мест
    if data["count_places"] <= 0:
        return jsonify({"error": "Count places must be positive"}), 400

    parking = Parking(
        address=data["address"],
        opened=data.get("opened", False),
        count_places=data["count_places"],
        count_available_places=data["count_places"],
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id}), 201


@api.route("/parkings", methods=["GET"])
def get_parkings():
    parkings = Parking.query.all()
    return (
        jsonify(
            [
                {
                    "address": c.address,
                    "opened": c.opened,
                    "count_places": c.count_places,
                }
                for c in parkings
            ]
        ),
        200,
    )


# заезд / выезд
@api.route("/client_parkings", methods=["POST"])
def enter_parking():
    data = request.json
    required_fields = ["client_id", "parking_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Проверка дублирования
    existing = ClientParking.query.filter_by(
        client_id=data["client_id"], parking_id=data["parking_id"], time_out=None
    ).first()
    if existing:
        return jsonify({"error": "Already parked"}), 400

    # Транзакция с блокировкой
    try:
        parking = db.session.execute(
            select(Parking).where(Parking.id == data["parking_id"]).with_for_update()
        ).scalar_one()

        if not parking.opened or parking.count_available_places <= 0:
            return jsonify({"error": "Parking unavailable"}), 400

        parking.count_available_places -= 1
        client_parking = ClientParking(
            client_id=data["client_id"],
            parking_id=data["parking_id"],
            time_in=datetime.now(),
        )
        db.session.add(client_parking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": True}), 200


@api.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    data = request.json
    client_parking = ClientParking.query.filter_by(
        client_id=data["client_id"], parking_id=data["parking_id"], time_out=None
    ).first_or_404()

    client = Client.query.get(data["client_id"])
    if not client.credit_card:
        return jsonify({"error": "No credit card linked"}), 400

    client_parking.time_out = datetime.now()
    parking = Parking.query.get(data["parking_id"])
    parking.count_available_places += 1

    # Защита от превышения лимита
    if parking.count_available_places > parking.count_places:
        parking.count_available_places = parking.count_places

    db.session.commit()
    return jsonify({"success": True}), 200
