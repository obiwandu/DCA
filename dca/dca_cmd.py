__author__ = 'User'
from util.datastructure import Identity


class DcaCmd:
    def __init__(self, control, ip, dev_id, dev_pw):
        self.control = control()
        self.identity = Identity()
        self.identity.ip = ip
        self.identity.dev_id = dev_id
        self.identity.dev_pw = dev_pw
        self.control.login(self.identity)
        return

    def logout(self):
        self.control.logout()
        return

    def execute(self, cmd):
        return self.control.exec_cmd(cmd)

def exec_command():
    return