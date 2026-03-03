from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Database
db = SQLAlchemy()

# LoginManager
log_in_man = LoginManager()
log_in_man.login_view = "main.landing"
