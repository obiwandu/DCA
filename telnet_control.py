from telnetlib import Telnet

__author__ = 'User'
from agent_control import AgentControl

class TelnetControl(AgentControl):
    def __init__(self):
        super(TelnetControl, self).__init__()
        self.tn = None

    def login(self, identity):
        self.tn = Telnet(identity.ip)
        print self.tn.read_until('Password:')
        self.tn.write(identity.dev_pw + "\n")
        # print tn.read_until("???", 5)
        print self.tn.read_until('>')
        return

    def exec_cmd(self, command):
        self.tn.write(command.act_cmd + "\n")
        feedback = self.tn.read_until('>')
        # self.tn.write('q\n'')
        self.tn.write('exit\n')
        # feedback = tn.read_until("???", 5)
        feedback = self.tn.read_until('>')
        print "feedback:", feedback
        return feedback

class TestTelnetControl(AgentControl):
    def __init__(self):
        super(TestTelnetControl, self).__init__()
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
        self.tn.write(command.act_cmd + "\n")
        feedback = self.tn.read_until('$', 5)
        # self.tn.write('q\n'')
        self.tn.write('exit\n')
        # feedback = tn.read_until("???", 5)
        print self.tn.read_until('$', 5)
        print "feedback:", feedback
        return feedback