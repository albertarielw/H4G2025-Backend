# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Dummy DB URL: postgresql://username:password@localhost/database
SQLALCHEMY_DATABASE_URI = 'postgresql://h4g:h4g@localhost/h4g'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# For session security, etc. — set your own secret key
SECRET_KEY = ''
