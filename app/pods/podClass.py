from kubernetes import client
from flask_login import current_user


class Pod(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = client.CoreV1Api()
        self.api_client = api_client
        self.username = current_user.username

    def all_list(self):
        pods = self.api_client.list_pod_for_all_namespaces(watch=False)
        return pods

    def get_list(self, label_selector=''):
        pods = self.api_client.list_namespaced_pod(self.username, label_selector=label_selector)
        return pods

    def exec(self):
        name = 'flaskdeploy-55c586b7bb-cc5wv'
        res = self.api_client.connect_post_namespaced_pod_exec(name, self.username, tty=True)
        return res

    def detail(self, name):
        return self.api_client.read_namespaced_pod(name, self.username, pretty='true')
