from paramiko import SSHClient, SSHException, BadHostKeyException, AuthenticationException
import paramiko
from agent_control import AgentControl
import socket

__author__ = 'User'

class SSHServerControl(AgentControl):
    """ Inherit from AgentControl. Implement all existing methods in the way of SSH.
    """
    def __init__(self):
        super(SSHServerControl, self).__init__()
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

    def login(self, identity):
        try:
            self.ssh.connect(identity.ip, username=identity.dev_id, password=identity.dev_pw)
            self.shell = self.ssh.invoke_shell()
            buf = ''
            while not (buf.endswith('$ ') or buf.endswith('# ')):
                buf += self.shell.recv(9999)
            print buf
        except BadHostKeyException, e:
            print '%s' % e
        except AuthenticationException, e:
            print '%s' % e
        except SSHException, e:
            print '%s' % e
        except socket.error, e:
            print '%s' % e
            return
        print 'log in'
        return

    def exec_cmd(self, command):
        self.shell.send(command + '\n')
        feedback = ''
        while not (feedback.endswith('$ ') or feedback.endswith('# ')):
            feedback += self.shell.recv(9999)
        print feedback
        return feedback

    def logout(self):
        self.shell.send('exit\n')
        feedback = self.shell.recv(9999)
        print feedback
        return