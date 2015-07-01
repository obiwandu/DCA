import eventlet
from template import Template
from eos.lib.http import HTTP
from telnetlib import Telnet
from new_template import TemplateNew
import re
from gevent.wsgi import WSGIServer
from datastructure import Identity, Command

__author__ = 'User'

class Handler:
    def __init__(self, env):
        print "msg being handling"
        # para = (msg['PATH_INFO']).split(";")
        # template, expect_result = Template.parse_temp(msg['PATH_INFO'])

        self.command, self.identity = Template.parse_xml(env['PATH_INFO'])
        self.command.show()
        self.identity.show()
        # self.msg_executor()
        # self.template = TemplateNew()
        # self.template.from_xml(env['PATH_INFO'])
        # self.template.show()
        # return self.msg_executor(template['ip'], template['userid'], template['pw'], template['act_cmd'])

        # feedback = self.msg_executor()
        return

    def test_executor(self):
        return ('name            time             size\n'
                 'file1           2015             10086\n'
                 'file1           2015             10086\n')

    def msg_executor(self):
        ip = self.identity.ip
        dev_pw = self.identity.dev_pw
        act_cmd = self.command.act_cmd
        # ip = self.template.exec_para['ip']
        # # dev_id = self.template.exec_para['dev_id']
        # dev_pw = self.template.exec_para['dev_pw']
        # act_cmd = self.template.cmd['act_cmd']
        tn = Telnet(ip)
        print tn.read_until("Password:")
        tn.write(dev_pw + "\n")
        print tn.read_until("???", 5)
        tn.write(act_cmd + "\n")
        tn.write("q\n")
        feedback = tn.read_until("???", 5)
        print "feedback:", feedback
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

def application(env, start_response):
    code = '200 OK'
    msg = 'SUCCESS'
    success = True

    print "new msg arrives"
    print env
    handler = Handler(env)
    feedback = handler.test_executor()
    result = handler.feedback_parser(feedback)
    # msg = self.msg_handler(env)

    start_response(code, [('Content-Type', 'text/plain')])

    # feedback = self.feedback_parser(msg)

    return ['%s\n' % str(result[0][0])]

if __name__ == "__main__":
    print 'Serving on 8000 starts...'
    server = WSGIServer(('', 8000), application).serve_forever()
