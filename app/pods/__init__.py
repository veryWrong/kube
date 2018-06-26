from flask import Blueprint

pod = Blueprint('pods', __name__)

from . import pods