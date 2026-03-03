# Import the libraries, classes and functions as necessary
import os
from flask import Flask
from werkzeug.security import generate_password_hash as gen_pass_h
from .extensions import db, log_in_man
from .models import User
from .config import Config
from .routes import main

def create_app():
    # Initialize the app
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )
    app.config.from_object(Config)

    # Initialize DB for the app
    db.init_app(app=app)

    # Initialize LoginManager for the app, along wit the user loader
    log_in_man.init_app(app=app)
    log_in_man.login_view = "main.landing"

    # Register the Route Blueprint
    app.register_blueprint(main)

    #create the databse and admin acc.
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        db.create_all()
        create_admin()

    return app

def create_admin() -> None:
    if not User.query.filter_by(u_email="admin@careergps.in").first():
        admin = User(
            u_name = "Administrator",
            u_email = "admin@careergps.in",
            u_role = "admin"
        )

        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully!\n")


