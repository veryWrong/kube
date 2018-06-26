import os
from kubernetes import config
from app.pods import pods

path = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    config.load_kube_config(path+'/config')
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/forward"




