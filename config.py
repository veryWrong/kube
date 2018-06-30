import os
from kubernetes import config

path = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    config.load_kube_config(path+'/config')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'kube.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True




