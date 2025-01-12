# main.py
from flask import Flask
from flask_cors import CORS

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import db

from login import login_bp
from users import users_bp
from items import items_bp
from tasks import tasks_bp
from usertasks import usertasks_bp
from itemrequests import itemrequests_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(usertasks_bp)
    app.register_blueprint(itemrequests_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5123)
