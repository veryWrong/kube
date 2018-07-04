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
@login_required
def node_list():
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    data = request.get_json()
    state = check_key('state', data)
    print(state)
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
        print(res)
    return jsonify({'code': 200, 'msg': 'ok', 'data': data})
    # return jsonify({'code': 200, 'msg': 'ok', 'data': [{
    #     'name': i.metadata.name,
    #     'ip': [m for m in i.status.addresses if m.type == 'InternalIP'],
    # } for i in res]})
