import json


def read_json(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def write_json(obj, path, **kw):
    params = {'ensure_ascii': False, 'indent': 2}
    params.update(kw)
    with open(path, 'w') as json_file:
        json.dump(obj, json_file, **params)
