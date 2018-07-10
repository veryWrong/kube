from kubernetes import client
from flask_login import login_required, current_user
from utils.utils import check_key, check_key_raise


@login_required
class Service(object):
    def __init__(self, api_client=None, body=None, data=None):
        if api_client is None:
            api_client = client.CoreV1Api()
        if body is None:
            body = client.V1Service()
        if data is None:
            raise Exception("data is None")
        self.data = data
        self.api_client = api_client
        self.body = body
        self.basic = check_key('lables', data, {'app': data['name'], 'namespace': current_user.username})

    def service_metadata(self):
        self.body.metadata = {
            'name': self.data['name'],
            'namespace': current_user.username,
            'lables': self.basic,
            'annotations': {'name': self.data['name'], 'namespace': current_user.username}
        }
        return self.body.metadata

    def service_spec(self):
        # check_key_raise('ports', self.data)
        ports = check_key('ports', self.data, [{}])
        nodePort = check_key('nodePort', ports[0], None)
        self.body.spec = dict(
            # [{"name": "https","protocol": "TCP","port": 443,"targetPort": 6443}]
            ports=check_key('ports', self.data, []),
            selector=self.basic,
            type=(None, "NodePort")[nodePort is not None]
        )
        return self.body.spec
