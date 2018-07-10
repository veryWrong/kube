
def check_key(key, data, default=None):
    """
    验证data.keys()是否包含key，如果是则返回data[key],否则返回None or default
    :param key: string or int ...
    :param data: dict or list ...
    :param default: mixed
    :return: mixed
    """
    if isinstance(data, dict):
        if key in data.keys():
            return data[key]
        else:
            return (None, default)[default is not None]
    return None


def check_key_raise(key, data):
    if isinstance(data, dict):
        if key in data.keys():
            return True
        else:
            raise Exception("'" + data.__str__() + "'object has no attribute'" + key + "'")
    raise Exception("'" + data.__str__ + "'object is not dict")
