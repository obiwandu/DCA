from eos.lib.http import HTTP
from device_mngt import DeviceManagemnt
from datastructure import Identity, Command
from user_interface.cmdline_interface import CmdLineInterface
import importlib
from template import Template
from cmd_script_executor import CmdSession
from client import MasterSelect
import gevent

class Master:
    def __init__(self, input_if, master_select):
        # init the input interface
        self.input_if = input_if()
        self.logged = False

        self.identity = Identity()
        self.command = Command()
        self.agent_ip = None
        self.master_select = master_select
        return

    def test(self):
        self.identity.ip =  '10.137.59.22'
        self.identity.dev_id = 'tianyi.dty'
        self.identity.dev_pw = 'Mtfbwy626488'
        dev = DeviceManagemnt()
        self.agent_ip = dev.get_devinfo(self.identity)
        command = Command()
        command.abs_cmd = 'ipconfig'

        template = Template()
        command = template.find(command.abs_cmd, self.identity)
        if command:
                str_xml = Template.to_xml(command, self.identity)
                return http_request(str_xml)
        return

    def login(self):
        self.input_if.login(self.identity)
        dev = DeviceManagemnt()
        self.agent_ip = dev.get_devinfo(self.identity)
        self.logged = True
        return

    def cfg_cmd(self):
        if self.logged:
            self.input_if.cfg_cmd(self.command)
            template = Template()
            template.to_template(self.command, self.identity)
        return

    def exec_cmd(self):
        if self.logged:
            abs_cmd = self.input_if.exec_cmd()
            template = Template()
            command = template.find(abs_cmd, self.identity)
            if command:
                str_xml = Template.to_xml(command, self.identity)
                # return http_request(str_xml)
                self.master_select.request(str_xml, self.agent_ip)
                return
        return

    # execute a single atomic command from parameter
    def exec_script_cmd(self, cmd):
        self.command.abs_cmd = cmd
        temp = Template()
        command = temp.find(cmd, self.identity)
        if command:
            str_xml = Template.to_xml(command, self.identity)
            # return http_request(str_xml)
            self.master_select.request(str_xml, self.agent_ip)
            return

    # execute a whole script containing atomic command(But execute separately)
    def exec_script(self):
        if self.logged:
            return self.input_if.exec_script()
        return

    def exec_script_by_transfer(self):
        script_name = self.input_if.exec_script()
        new_script_name, self.agent_ip = CmdSession.translate_script(script_name)
        try:
            fp = open(new_script_name, 'r')
        except IOError, e:
            print 'Script file %s not found.' % e
            return
        str_script = fp.read()
        str_xml = Template.to_xml(None, None, str_script)
        # return http_request(str_xml)
        self.master_select.request(str_xml, self.agent_ip)
        return

    def show_temp(self):
        # print self.temp.tempDict
        return

def http_request(template_str):
    http_client = None
    ret = ""
    try:
        uri = template_str
        # ret = HTTP("0.0.0.0", 8000).get(uri)
        ret = HTTP("127.0.0.1", 8000).get(uri)

        # print "**************************"
        # print "start printing response:"
        # print ret
        # print "**************************"

    except Exception, e:
        print "Print exception:"
        print e
    finally:
        if http_client:
            http_client.close()
    return ret

def start_master2():
    master = Master(CmdLineInterface)
    master.login()
    while True:
        opr_type = raw_input("operation type:")
        # if opr_type == "cfg":
        #     master.cfg_cmd()
        # elif opr_type == "exec":
        #     master.exec_cmd()
        if opr_type == "show temp":
            master.show_temp()
        elif opr_type == "cfg":
            master.cfg_cmd()
        elif opr_type == "exec":
            master.exec_cmd()
        elif opr_type == "test":
            master.test()
        elif opr_type == "script":
            master.exec_script()

def master_process(master_select):
    while True:
        gevent.sleep(1)
        opr_type = raw_input('operation type:')
        if opr_type == 'show temp':
            master.show_temp()
        elif opr_type == 'cfg':
            # master_select = MasterSelect()
            master = Master(CmdLineInterface, master_select)
            master.login()
            master.cfg_cmd()
        elif opr_type == 'exec':
            # master_select = MasterSelect()
            master = Master(CmdLineInterface, master_select)
            master.login()
            master.exec_cmd()
        elif opr_type == 'test':
            master.test()
        elif opr_type == 'script':
            # master_select = MasterSelect()
            master = Master(CmdLineInterface, master_select)
            master.exec_script_by_transfer()
        elif opr_type == 'script_old':
            master.login()
            script_name = master.exec_script()
            new_script_name = CmdSession.load_script(script_name)
            new_script_name = new_script_name.split('.')
            importlib.import_module(new_script_name[0])

def test_process(master_select):
    master = Master(CmdLineInterface, master_select)
    master.exec_script_by_transfer()

if __name__ == "__main__":
    master_select = MasterSelect()
    listen = gevent.spawn(master_select.listen)
    req = gevent.spawn(master_process, master_select)
    gevent.joinall([listen, req])
