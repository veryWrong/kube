from flask import jsonify, request
from flask_login import login_required, current_user
from kubernetes.client.rest import ApiException
from .deployClass import Deploy
from ..pods.podClass import Pod
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


@deploy.route('/detail/<string:name>', methods=['GET'])
@login_required
def get_detail(name):
    try:
        detail, select = Deploy(data={}).detail(name), ''
        for k, v in detail.metadata.labels.items():
            select += k + '=' + v + ','
        pods, pod_detail, pod_info = Pod().get_list(label_selector=select[:-1]), {}, []
        for i, p in enumerate(pods.items):
            pod_info.append({
                'name': p.metadata.name,
                'state': p.status.phase,
                'pod_ip': p.status.pod_ip,
                'create_time': p.status.start_time,
            })
        pod = Pod().detail(pods.items[0].metadata.name)
        pod_detail = {
            'name': detail.metadata.name,
            'create_time': detail.metadata.creation_timestamp,
            'image': detail.spec.template.spec.containers[0].image,
            'pod_info': pod_info,
            'resources': pod.spec.containers[0].resources.limits,
            'env': pod.spec.containers[0].env,
            'command': pod.spec.containers[0].command,
            'ports': [{
                'container_port': i.container_port,
                'protocol': i.protocol,
            } for i in pod.spec.containers[0].ports if len(pod.spec.containers[0].ports) > 0],
        }
        if detail.status.conditions[-1].type == Deploy.DeploymentAvailable:
            pod_detail['status'] = 'runing'
        elif detail.status.conditions[-1].type == Deploy.DeploymentProgressing:
            pod_detail['status'] = 'pending'
        else:
            pod_detail['status'] = 'stoped'
        return jsonify({'code': 200, 'msg': 'ok', 'data': pod_detail})
    except ApiException as e:
        return jsonify({'code': 500, 'msg': 'error', 'data': eval(e.body)['message']})
