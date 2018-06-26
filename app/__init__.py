from flask import Flask
from config import DevConfig
from app.pods import pods


def init_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    return app
