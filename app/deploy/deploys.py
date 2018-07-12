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
    tty = 'true'
    try:
        deploy_api_res = deploy.api_client.create_namespaced_deployment(current_user.username, deploy.body, pretty=tty)
        print(deploy_api_res)
        service_api_res = service.api_client.create_namespaced_service(current_user.username, service.body, pretty=tty)
        print(service_api_res)
        return jsonify({'code': 200, 'msg': '创建成功'})
    except ApiException as e:
        print(eval(e.body))
        return jsonify({'code': 500, 'msg': '创建失败', 'data': eval(e.body)['message']})


@deploy.route('/list', methods=['GET'])
@login_required
def get_list():
    deploys = Deploy(data={}).get_list()
    print(deploys)
    return jsonify({'code': 200, 'msg': 'ok', 'data': [{
        'name': i.metadata.name,
        'replicas': i.spec.replicas,
        'available_replicas': i.status.available_replicas,
        'image': i.spec.template.spec.containers[0].image
    } for i in deploys.items]})


@deploy.route('/delete/<string:name>', methods=['GET'])
@login_required
def delete(name):
    deploy = Deploy(data={})
    service = Service(data={})
    try:
        deploy_api_res = deploy.delete(name)
        print(deploy_api_res)
        service_api_res = service.delete(name)
        print(service_api_res)
        return jsonify({'code': 200, 'msg': '删除成功'})
    except ApiException as e:
        print(eval(e.body))
        return jsonify({'code': 500, 'msg': '删除失败', 'data': eval(e.body)['message']})

