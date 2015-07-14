from control_protocol.agent_control import AgentControl

__author__ = 'User'

class TelnetStubControl(AgentControl):
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