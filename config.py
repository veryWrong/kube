import os
from kubernetes import config

path = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "\x143\x1a\xb1e\x9e\xa8gR\xf1\x97\xb9)gw\x9a\x14&\xdc\tZ\xd2]\xa9"
    TOKEN_VALIDITY_PERIOD = 14400  # token过期时间
    config.load_kube_config(path + '/config')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'kube.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
