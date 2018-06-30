from kubernetes import client
from flask import jsonify
from . import node


@node.route('/list', methods=['GET'])
def node_list():
    v1 = client.CoreV1Api()
    ret = v1.list_node()
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
