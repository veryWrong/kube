from kubernetes import client
from flask import jsonify
from . import pod


@pod.route('/', methods=['GET', ])
def index():
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    return jsonify({'code': 200, 'msg': '成功获取所有pod', 'data': [{
        "podIp": i.status.pod_ip,
        "namespace": i.metadata.namespace,
        "podName": i.metadata.name,
    } for i in ret.items]})
