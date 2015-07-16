from control_protocol.agent_control import AgentControl

__author__ = 'User'

class TelnetStubControl(AgentControl):
    """ Inherit from AgentControl. Implement all existing methods only for test the translation of the same abstract
        commands on different real devices.
    """
    def __init__(self):
        super(TelnetStubControl, self).__init__()
        self.tn = None

    def login(self, identity):
        print "login successfully"
        return

    def exec_cmd(self, command):
        print "command %s is going to be executed" % command
        return "successfully"

    def logout(self):
        return