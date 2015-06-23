from eos.lib.hub import WSGIServer, StreamServer
from eos.lib import hub
import eventlet
from template import Template
from eos.lib.http import HTTP
from telnetlib import Telnet
test
class Agent:
    def __init__(self):
        return

    def start_service(self):
        services = []

        server = Server()
        listen_thread = hub.spawn(server)

        services.append(listen_thread)

        hub.joinall(services)
        return

class MsgHandler(object):
    def __init__(self):
        super(MsgHandler, self).__init__()

        self.is_active = True
        self.ports = None
        self.set_state('DISPATCH')

    def close(self):
        self.set_state('CLOSE_DISPATCH')

    def set_state(self, state):
        self.state = state

    def set_version(self, version):
        self.version = version

    # Low level socket handling layer
    def __call__(self, env, start_response):
        eventlet.sleep(0.1)

        code = '200 OK'
        msg = 'SUCCESS'
        success = True
        # for k, v in env.items():
            # print '%s: %s' % (k, v)

        # md5 = env.get('HTTP_MD5SUM', "")

        # if env['PATH_INFO'] != '/':
        #     code = '404 Not Found'
        #     msg = 'Not Found'
        #     success = False

        hub.sleep(0)

        print "new msg arrives"
        msg = self.msg_handler(env)

        start_response(code, [('Content-Type', 'text/plain')])

        print "msg:"
        print msg

        feedback = self.feedback_parser(msg)

        return ['%s\n' % str(msg)]

    def msg_handler(self, msg):
        print "msg being handling"
        # para = (msg['PATH_INFO']).split(";")
        template = Template.parse_temp(msg['PATH_INFO'])
        print template
        print "execute cmd: %s" % template['act_cmd']
        return self.msg_executor(template['ip'], template['userid'], template['pw'], template['act_cmd'])

    @staticmethod
    def msg_executor(ip, userid, pw, cmd):
        # tn = Telnet(ip)
        # tn.read_until("login: ")
        # tn.write(userid + "\n")
        # tn.read_until("Password: ")
        # tn.write(pw + "\n")
        # tn.write(cmd + "\n")
        # tn.write("exit\n")
        # feefback = tn.read_all()

        # pw = "huawei123"
        # tn = Telnet("10.65.254.70")
        tn = Telnet(ip)
        print tn.read_until("Password:")
        tn.write(pw + "\n")
        print tn.read_until("???", 5)
        tn.write(cmd + "\n")
        tn.write("q\n")
        feedback = tn.read_until("???", 5)
        print "feedback:"
        print feedback
        return feedback

    @staticmethod
    def feedback_parser(feedback):

        return

def http_request(cmd, ip):
    httpClient = None
    try:
        uri = cmd
        ret = HTTP(ip, 8000).get(uri)

        print "**************************"
        print "start printing response:"
        print ret
        print "**************************"

    except Exception, e:
        print "Print exception:"
        print e
    finally:
        if httpClient:
            httpClient.close()
    return

class Server(object):
    def __init__(self):
        super(Server, self).__init__()
        self.msg_handler = MsgHandler()
        # self.daemon_thread = hub.spawn(self.agent_daemon)
        # self.work_threads = 0
        self.count = 0

    # entry point
    def __call__(self):
        #LOG.debug('call')
        self.server_loop()
        pass

    def server_loop(self):
        server = WSGIServer(('', 8000), self.msg_handler)

        #LOG.debug('loop')
        server.serve_forever()

# def main_procedure():
#
#     services = []
#
#     server = Server()
#     listen_thread = hub.spawn(server)
#
#     services.append(listen_thread)
#
#     hub.joinall(services)

if __name__ == "__main__":
    # main_procedure()
    agent = Agent()
    agent.start_service()