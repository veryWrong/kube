from flask import Blueprint

deploy = Blueprint('deploy', __name__)

from . import deploys

