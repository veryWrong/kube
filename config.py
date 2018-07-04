import os
from kubernetes import config

path = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "kube"
    TOKEN_VALIDITY_PERIOD = 14400
    config.load_kube_config(path+'/config')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'kube.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True




