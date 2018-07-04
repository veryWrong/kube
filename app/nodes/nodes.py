from kubernetes import client
from flask import jsonify, request
from flask_login import login_required
from utils.utils import check_key
from . import node


@node.route('/', methods=['GET'])
@login_required
def node_count():
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    print(ret)
    count = len(ret.items)
    online, offline, unknown = 0, 0, 0
    for res in ret.items:
        if res.status.conditions[-1].status == "True":
            online += 1
        elif res.status.conditions[-1].status == "False":
            offline += 1
        else:
            unknown += 1
    data = {
        'count': count,
        'online': online,
        'offline': offline,
        'unknown': unknown,
    }
    return jsonify({'code': 200, 'msg': 'ok', 'data': data})


@node.route("/list", methods=['GET'])
# @login_required
def node_list():
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    data = request.get_json()
    state = check_key('state', data)
    if state is not None and state == 'online':
        res = []
        for item in ret.items:
            if item.status.conditions[-1].status == "True":
                res.append(item)
    elif state is not None and state == 'offline':
        res = []
        for item in ret.items:
            if item.status.conditions[-1].status == "False":
                res.append(item)
    else:
        res = ret.items
    return jsonify({'code': 200, 'msg': 'ok', 'data': [{
        'name': i.metadata.name,
        'ip': i.status.addresses[0].address,
        'image': i.status.node_info.os_image,
        'version': i.status.node_info.kernel_version,
        'cpu': i.status.allocatable['cpu'],
        'memory': int(i.status.allocatable['memory'][0:-2]) / 1024 / 1024,
        'create_time': i.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    } for i in res]})
