from flask import Flask
from flask_login import LoginManager
from config import DevConfig
from app.pods import pods


login_manager = LoginManager()
login_manager.session_protection = 'strong'


def init_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    login_manager.init_app(app)
    return app
