# main.py
from flask import Flask
from config import BaseConfig
from configure_extensions import configure_extensions
from models import db

from login import login_bp
from users import users_bp
from items import items_bp
from tasks import tasks_bp
from usertasks import usertasks_bp
from transcations import transactions_bp
from logs import logs_bp


def create_app(config_class=BaseConfig):
    # Create the Flask app
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Initialize extensions (e.g., SQLAlchemy, etc.)
    configure_extensions(flask_app)

    # Register Blueprints
    flask_app.register_blueprint(login_bp)
    flask_app.register_blueprint(users_bp)
    flask_app.register_blueprint(items_bp)
    flask_app.register_blueprint(tasks_bp)
    flask_app.register_blueprint(usertasks_bp)
    flask_app.register_blueprint(transactions_bp)
    flask_app.register_blueprint(logs_bp)

    # Create database tables on every startup (optional)
    with flask_app.app_context():
        db.create_all()

    return flask_app


# Create a top-level 'app' that Gunicorn can import
app = create_app()


if __name__ == "__main__":
    # If you're running locally for debugging:
    app.run(debug=True, host="0.0.0.0", port=5123)
