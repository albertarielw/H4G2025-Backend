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
from itemrequests import itemrequests_bp


def create_app(config_class=BaseConfig):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    configure_extensions(flask_app)

    # Register Blueprints
    flask_app.register_blueprint(login_bp)
    flask_app.register_blueprint(users_bp)
    flask_app.register_blueprint(items_bp)
    flask_app.register_blueprint(tasks_bp)
    flask_app.register_blueprint(usertasks_bp)
    flask_app.register_blueprint(itemrequests_bp)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5123)
