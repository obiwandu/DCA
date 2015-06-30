from datastructure import Identity
from datastructure import Command

class DeviceManagemnt:
    def __init__(self):
        return

    def get_devinfo(self, identity):
        identity.dev_type = 'switch'
        identity.dev_factory = 'HW'
        identity.dev_model = '150'
        return
