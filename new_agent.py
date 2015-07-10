from template import Template
import re
from gevent.wsgi import WSGIServer
from gevent.server import StreamServer
from control_protocol.telnet_control import TelnetControl, TestTelnetControl

__author__ = 'User'

class Handler:
    def __init__(self, data, control):
        print "msg being handling..."
        self.control = control()
        # self.command, self.identity, self.script = Template.parse_xml(env['PATH_INFO'])
        self.command, self.identity, self.script = Template.parse_xml(data)
        if not self.script:
            self.type = 'cmd'
            self.command.show()
            self.identity.show()
        else:
            self.type = 'script'
            self.script_name = 'temp_script\\temp_agent_script.py'
            file = open(self.script_name, 'w')
            file.write(self.script)
            file.close()
        return

    def test_executor(self):
        return ('name            time             size\n'
                 'file1           2015             10086\n'
                 'file1           2015             10086\n')

    def msg_executor(self):
        if self.type == 'cmd':
            self.control.login(self.identity)
            feedback = self.control.exec_cmd(self.command.act_cmd)
        elif self.type == 'script':
            # feedback = self.control.exec_script(self.script)
            result = dict()
            execfile(self.script_name, dict(), result)
            feedback = result['script_ret']
        else:
            feedback = 'not handled'
        return feedback

    def feedback_parser(self, feedback):
        # exp_res = self.template.exp_res
        exp_res = self.command.exp_result
        if exp_res:
            final_res = []
            for key, regex in exp_res:
                print key, regex
                match_res = re.findall(regex, feedback)
                print match_res
                final_res.append((key, match_res))
                # final_res.append((key, re.match(regex, feedback).group()))
            return final_res
        else:
            return

def application(socket, address):
    code = '200 OK'
    msg = 'SUCCESS'
    success = True

    data = socket.recv(4096)
    print "new msg arrives"
    print data
    handler = Handler(data, TestTelnetControl)
    msg = handler.msg_executor()
    # start_response(code, [('Content-Type', 'text/plain')])
    print 'start to send feedback', msg
    socket.sendall(msg)

    return
    # return ['%s\n' % str(msg)]

if __name__ == "__main__":
    print 'Serving on 8000 starts...'
    # server = WSGIServer(('', 8000), application).serve_forever()
    server = StreamServer(('', 8000), application).serve_forever()
