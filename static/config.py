import os
import secrets
super_rando = secrets.token_hex(50)
class Config:
    SECRET_KEY = str(super_rando)
    SQLALCHEMY_DATABASE_URI = "sqlite:///databse.db"
    SQLAlchemy_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 #5-mb
