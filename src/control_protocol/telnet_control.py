from telnetlib import Telnet
from agent_control import AgentControl

__author__ = 'User'

class TelnetControl(AgentControl):
    """ Inherit from AgentControl. Implement all existing methods in the way of Telnet.
    """
    def __init__(self):
        super(TelnetControl, self).__init__()
        self.tn = None

    def login(self, identity):
        self.tn = Telnet(identity.ip)
        print self.tn.read_until('Password:')
        self.tn.write(identity.dev_pw + "\n")
        print self.tn.read_until('>')
        return

    def exec_cmd(self, command):
        self.tn.write(command.act_cmd + "\n")
        feedback = self.tn.read_until('>')
        print "feedback:", feedback
        return feedback

    def logout(self):
        self.tn.write('exit\n')
        return
