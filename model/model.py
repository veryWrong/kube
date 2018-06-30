from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from manage import db


class User(db.Model):
    __tablename__ = 'adm_user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(25), unique=True, index=True)
    password = db.Column(db.String(128), unique=True,)
    email = db.Column(db.String(32), index=True)
    role = db.Column(db.String(15), unique=True, default="")
    create_date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username):
        self.username = username

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def __repr__(self):
        return "<User `{}`".format(self.username)
