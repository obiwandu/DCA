from telnetlib import Telnet
from agent_control import AgentControl

__author__ = 'User'

class TelnetServerControl(AgentControl):
    """ Inherit from AgentControl. Implement all existing methods in the way of Telnet.
        It's meant to interact with a linux server instead of a network device.
    """
    def __init__(self):
        super(TelnetServerControl, self).__init__()
        self.tn = None

    def login(self, identity):
        self.tn = Telnet(identity.ip)
        print self.tn.read_until("login: ")
        self.tn.write(identity.dev_id + "\n")
        print self.tn.read_until("Password: ")
        self.tn.write(identity.dev_pw + "\n")
        feedback = self.tn.read_until('$', 5)
        return

    def exec_cmd(self, command):
        self.tn.write(command + "\n")
        feedback = self.tn.read_until('$', 5)
        print "feedback:", feedback
        return feedback

    def logout(self):
        self.tn.write('exit\n')
        print self.tn.read_until('$', 5)
        return