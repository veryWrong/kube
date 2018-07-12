from kubernetes import client
from datetime import datetime
from flask_login import current_user
from utils.utils import check_key, check_key_raise


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
        self.username = current_user.username
        self.basic = check_key('lables', data, {'app': check_key('name', data), 'namespace': self.username})

    def deploy_metadata(self):
        check_key_raise('name', self.data)
        self.body.metadata = {
            'name': self.data['name'],
            'namespace': self.username,
            'lables': self.basic,
            'annotations': {
                'name': self.data['name'],
                'namespace': self.username,
                'create_date': datetime.now()
            }
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

    def get_list(self):
        deploys = self.api_client.list_namespaced_deployment(self.username)
        return deploys

    def delete(self, name):
        body = client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=5)
        res = self.api_client.delete_namespaced_deployment(name=name, namespace=self.username, body=body, pretty='true')
        return res
