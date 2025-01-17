# config.py
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # Dummy DB URL: postgresql://username:password@localhost/database
    database_url = os.getenv('DB_URI')
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # For session security, etc. — set your own secret key
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "H4G_oh_so_safe")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
