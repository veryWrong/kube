from flask import jsonify, request
from flask_login import login_required, current_user
from kubernetes.client.rest import ApiException
from .deployClass import Deploy
from ..service.serviceClass import Service
from . import deploy


@deploy.route('/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    deploy = Deploy(data=data)
    deploy.body.metadata = deploy.deploy_metadata()
    deploy.body.spec = deploy.deploy_spec()
    service = Service(data=data)
    service.body.metadata = service.service_metadata()
    service.body.spec = service.service_spec()
    try:
        deploy_api_res = deploy.api_client.create_namespaced_deployment(current_user.username, deploy.body, pretty=True)
        print(deploy_api_res)
        service_api_res = service.api_client.create_namespaced_service(current_user.username, service.body, pretty=True)
        print(service_api_res)
        return jsonify({'code': 200, 'msg': '创建成功'})
    except ApiException as e:
        print(eval(e.body))
        return jsonify({'code': 500, 'msg': '创建失败', 'data': eval(e.body)['message']})
