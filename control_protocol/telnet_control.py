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
        self.tn.write(command + "\n")
        feedback = self.tn.read_until('$', 5)
        print "feedback:", feedback
        return feedback

    def logout(self):
        self.tn.write('exit\n')
        print self.tn.read_until('$', 5)
        return

class TestScriptControl(AgentControl):
    def __init__(self):
        super(TestScriptControl, self).__init__()
        self.tn = None

    def login(self, identity):
        print "login successfully"
        return

    def exec_cmd(self, command):
        print "command %s is going to be executed" % command
        return "successfully"

    def logout(self):
        return