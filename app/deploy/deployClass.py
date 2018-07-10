from kubernetes import client
from flask_login import login_required, current_user
from utils.utils import check_key


@login_required
class Deploy(object):
    def __init__(self, api_client=None, body=None, data=None):
        if api_client is None:
            api_client = client.ExtensionsV1beta1Api()
        if body is None:
            body = client.V1Deployment()
        if data is None:
            raise Exception("data is None")
        self.data = data
        self.api_client = api_client
        self.body = body
        self.basic = check_key('lables', data, {'app': data['name'], 'namespace': current_user.username})

    def deploy_metadata(self):
        self.body.metadata = {
            'name': self.data['name'],
            'namespace': current_user.username,
            'lables': self.basic,
            'annotations': {'name': self.data['name'], 'namespace': current_user.username}
        }
        return self.body.metadata

    def deploy_spec(self):
        self.body.spec = {
            'replicas': check_key('replicas', self.data, 1), 'selector': {
                'matchLabels': self.basic,
            },
            'template': {
                'metadata': {
                    'labels': self.basic,
                },
                'spec': {
                    'containers': [
                        {
                            'name': self.data['name'],
                            'image': self.data['image'],
                            'command': check_key('command', self.data, []),
                            # [{"containerPort": 80, "protocol": "TCP"}]
                            'ports': check_key('deploy_ports', self.data, None),
                            'resources': {
                                # requests资源的最小申请量，limits资源最大允许使用量
                                'requests': check_key('requests', self.data, {'cpu': '0.05', 'memory': '16Mi'}),
                                'limits': check_key('limits', self.data, {'cpu': '0.1', 'memory': '1Gi'}),
                            },
                            'imagePullPolicy': check_key('imagePullPolicy', self.data, 'IfNotPresent'),
                            'restartPolicy': check_key('restartPolicy', self.data, 'Always'),
                            # [{"name": "MYSQL_SERVICE_HOST", "value": "mysql"}]
                            'env': check_key('env', self.data, None),
                        }
                    ]
                }
            }
        }
        return self.body.spec
