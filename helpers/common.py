import json

def create_request(type, data):
    obj = {}
    obj["type"] = type

    if data != None:
        obj["data"] = data

    return json.dumps(obj).encode('utf-8')