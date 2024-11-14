import json

def create_request(type, data):
    obj = {}
    obj["type"] = type

    if data != None:
        obj["data"] = data

    return json.dumps(obj).encode('utf-8')

def handle_receive_data(self, data):
    print('receive', data)
    if data:
        self.root.after(0, update_display, self, data)

def update_display(self, data):
    pass