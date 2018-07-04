from kubernetes import client
from flask import jsonify
from flask_login import login_required
from . import pod


@pod.route('/', methods=['GET', ])
@login_required
def pod_count():
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    online, offline = 0, 0
    for i in ret.items:
        item = i.status.container_statuses[-1]
        if item.ready is True and item.state.running is not None:
            online += 1
        else:
            offline += 1
    return jsonify({'code': 200, 'msg': '成功获取所有pod', 'data': {
        'count': len(ret.items),
        'online': online,
        'offline': offline,
    }})
