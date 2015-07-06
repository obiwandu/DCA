from datastructure import Identity
from datastructure import Command

class DeviceManagemnt:
    def __init__(self):
        return

    def get_devinfo(self, identity):
        if identity.ip == '1.1.1.1':
            identity.dev_type = 'switch'
            identity.dev_factory = 'HW'
            identity.dev_model = '150'
        elif identity.ip == '192.168.0.1':
            identity.dev_type = 'switch'
            identity.dev_factory = 'CISCO'
            identity.dev_model = '200'
        else:
            identity.dev_type = 'switch'
            identity.dev_factory = 'HW'
            identity.dev_model = '150'
        return
