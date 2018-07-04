from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_login import UserMixin
from manage import db
from config import DevConfig


class User(UserMixin, db.Model):
    # noinspection SpellCheckingInspection
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

    def generate_auth_token(self, expiration=DevConfig.TOKEN_VALIDITY_PERIOD):
        s = Serializer(DevConfig.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(DevConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return "<User `{}`".format(self.username)
