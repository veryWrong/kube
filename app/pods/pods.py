from kubernetes import client
from flask import jsonify
from . import pod


@pod.route('/', methods=['GET', ])
def index():
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    return jsonify({'code': 200, 'msg': '项目启动成功', 'data': ret})
