from kubernetes import client
from flask import jsonify, request
from flask_login import login_required, current_user
from kubernetes.client.rest import ApiException
from utils.utils import check_key
from config import DevConfig
from . import deploy


@deploy.route('/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    v1 = client.ExtensionsV1beta1Api()
    basic = check_key('lables', data, {'app': data['name'], 'namespace': current_user.username})
    body = client.V1Deployment()
    body.api_version = DevConfig.DEPLOY_API_VERSION
    body.kind = 'Deployment'
    body.metadata = dict(name=data['name'], namespace=current_user.username, lables=basic, annotations={
        'name': data['name'], 'namespace': current_user.username
    })
    body.spec = {'replicas': check_key('replicas', data, 1), 'selector': {
        'matchLabels': basic,
    }, 'template': {
        'metadata': {
            'labels': basic,
        },
        'spec': {
            'containers': [
                {
                    'name': data['name'],
                    'image': data['image'],
                    'command': check_key('command', data, []),
                    'ports': check_key('ports', data, None),  # [{"containerPort": 80, "protocol": "TCP"}]
                    'resources': {
                        # requests资源的最小申请量，limits资源最大允许使用量
                        'requests': check_key('requests', data, {'cpu': '0.05', 'memory': '16Mi'}),
                        'limits': check_key('limits', data, {'cpu': '1', 'memory': '1Gi'}),
                    },
                    'imagePullPolicy': check_key('imagePullPolicy', data, 'IfNotPresent'),
                    'restartPolicy': check_key('restartPolicy', data, 'Always'),
                    'env': check_key('env', data, None),  # [{"name": "MYSQL_SERVICE_HOST", "value": "mysql"}]
                }
            ]
        }
    }}
    # print(body)
    try:
        api_response = v1.create_namespaced_deployment(current_user.username, body, pretty=True)
        print(api_response)
        return jsonify({'code': 200, 'msg': '创建成功'})
    except ApiException as e:
        print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)
    return jsonify({'code': 500, 'msg': '创建失败'})
