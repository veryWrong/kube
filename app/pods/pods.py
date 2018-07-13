from flask import jsonify
from flask_login import login_required
from .podClass import Pod
from . import pod


@pod.route('/', methods=['GET', ])
@login_required
def pod_count():
    ret = Pod().all_list()
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


@pod.route('/exec', methods=['POST', ])
@login_required
def tty():
    res = Pod().exec()
    print(res)
    return jsonify({'code': 200, 'msg': 'ok'})
