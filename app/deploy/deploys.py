from kubernetes import client
from flask import jsonify, request
from flask_login import login_required
from utils.utils import check_key
from . import deploy


@deploy.route('/create', methods=['POST'])
def create():
    v1 = client.CoreV1Api()
    namespace = 'flask'
    body = client.V1Deployment()
    body.kind = 'Deployment'
