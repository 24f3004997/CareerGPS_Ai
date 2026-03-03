# Imports
from .extensions import db, log_in_man
from flask_login import UserMixin
from werkzeug.security import generate_password_hash as gen_pass_h
from werkzeug.security import check_password_hash as check_pass

#define User Loader
@log_in_man.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))

# User Model
class User(db.Model, UserMixin):
    # User Table Columns
    u_id = db.Column(
        db.Integer, 
        primary_key=True
    )
    u_name = db.Column(
        db.String(180), 
        nullable=False
    )
    u_email = db.Column(
        db.String(180), 
        nullable=False, 
        unique=True
    )
    password_hashed = db.Column(
        db.String(200), 
        nullable=False
    )
    u_role = db.Column(
        db.String(20), 
        nullable=False, 
        default="user"
    )
    u_resume_path = db.Column(
        db.String(500),
        nullable=True
    )

    def get_id(self):
        return str(self.u_id)
    
    def set_password(self, pass_h) -> None:
        self.password_hashed = gen_pass_h(pass_h)
    
    def check_password(self, pass_h) -> bool:
        return check_pass(self.password_hashed, pass_h)
    
    def is_admin(self) -> bool:
        return self.u_role == "admin"
