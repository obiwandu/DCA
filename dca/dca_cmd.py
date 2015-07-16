__author__ = 'User'
from util.datastructure import Identity


class DcaCmd:
    """ Define the way how the command in script executed on agent
    """
    def __init__(self, control, ip, dev_id, dev_pw):
        self.control = control()    # initialize the control protocol
        self.identity = Identity()
        self.identity.ip = ip
        self.identity.dev_id = dev_id
        self.identity.dev_pw = dev_pw
        self.control.login(self.identity)   # log in remote device in the way specified by protocol
        return

    def logout(self):
        """ log out from remote device in the way specified by protocol
        """
        self.control.logout()
        return

    def execute(self, cmd):
        """ execute the command on remote device in the way specified by protocol
        """
        return self.control.exec_cmd(cmd)
