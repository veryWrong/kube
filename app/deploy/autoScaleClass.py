from kubernetes import client
from datetime import datetime
from flask_login import current_user
from utils.utils import check_key, check_key_raise


def scale_target_ref(name):
    return {
        'scaleTargetRef': {
            'apiVersion': 'autoscaling/v2beta1',
            'kind': 'Deployment',
            'name': name,
        }
    }


class AutoScale(object):

    def __init__(self, api_client=None, body=None, data=None):
        if api_client is None:
            api_client = client.AutoscalingV2beta1Api()
        if body is None:
            body = client.V2beta1HorizontalPodAutoscaler()
        if data is None:
            raise Exception("data is None")
        self.data = data
        self.api_client = api_client
        self.body = body
        self.username = current_user.username
        self.basic = check_key('lables', data, {'app': check_key('name', data), 'namespace': self.username})

    def auto_scale_metadata(self):
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

    def auto_scale_spec(self):
        self.body.spec = {
            'maxReplicas': check_key_raise('maxReplicas', self.data),
            'minReplicas': check_key_raise('minReplicas', self.data),
            'scaleTargetRef': scale_target_ref(check_key_raise('name', self.data)),
            'metrics': [{
                'type': check_key('type', self.data, 'Resource'),
                'resource': {
                    'name': check_key('resource_name', self.data, 'cpu'),
                    'targetAverageUtilization': check_key_raise('cpu_threshold', self.data),
                }
            }]
        }
        return self.body.spec
