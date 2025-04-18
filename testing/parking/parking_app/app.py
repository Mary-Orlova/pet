from flask import Flask

from .database import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Отложенная инициализация
    db.init_app(app)

    # Регистрация teardown-обработчика
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            db.session.rollback()  # Откат при ошибке
        db.session.remove()  # Всегда удаляем сессию

    # Регистрация блюпринта
    from .routes import api

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
