__author__ = 'User'

import re

from util.template_handler import TemplateHandler
from device.device_mngt import DeviceManagemnt
from util.datastructure import Identity


class ScriptHandler:
    def __init__(self):
        return

    def exec_script(self):
        exec(open('script.py').read())

    @staticmethod
    def make_executable(cmd):
        return "master.exec_script_cmd('" + cmd + "')"

    @staticmethod
    def generate_script(abs_cmd, identity, protocol):
        script_template = "from dca.dca_cmd import DcaCmd\n" \
                   "from control_protocol.telnet_control import {class_name}\n" \
                   "dev1 = DcaCmd({class_name}, '{ip}', '{dev_id}', '{dev_pw}')\n" \
                   "script_ret = dev1.execute('{cmd}')\n" \
                   "dev1.logout()"
        script = script_template.format(class_name=protocol.__name__, ip=identity.ip, \
                                 dev_id=identity.dev_id, dev_pw=identity.dev_pw, cmd=abs_cmd)
        return script

    @staticmethod
    def translate_script(str_script):
        # find all keywords
        try:
            fp = open('template\\template.xml', 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return

        cmd = []
        temp_no = 1
        for line in fp:
            temp_no += 1
            command, dev_info = TemplateHandler.parse_template(line)
            cmd.append((command.abs_cmd, command.act_cmd, dev_info.dev_type, dev_info.dev_factory, dev_info.dev_model))

        #translate original script
        str_script_translated = ''

        device = dict()
        ip = []
        agent_ip = None
        for line in str_script:
            if 'DcaCmd(' in line:
                var_name, exp = line.replace(' ', '').split('=')
                result = re.findall("'.*?'", exp)
                identity = Identity()
                identity.ip = result[0][1:-1]
                identity.dev_id = result[1][1:-1]
                identity.dev_pw = result[2][1:-1]
                temp_agent_ip, dev_info = DeviceManagemnt.get_devinfo(identity.ip)
                if not agent_ip:
                     agent_ip = temp_agent_ip
                else:
                    if temp_agent_ip != agent_ip:
                        print "devices don't belong to one unique agent"
                        return
                device[var_name] = dev_info
                ip.append(identity.ip)

        line_no = 1
        for line in str_script:
            line_no += 1
            if 'execute' in line:
                # restriction: there must be space between operator and variables/methods.
                # This is coincident with standard of Python programming style
                for exp in line.split():
                    if 'execute' in exp:
                        var_name, method = exp.replace(' ', '').split('.')
                        dev = device[var_name]
                        result = re.search("'.*?'", method).group()[1:-1]
                        for abs_cmd, act_cmd, dev_type, dev_factory, dev_model in cmd:
                            if abs_cmd == result and dev.dev_type == dev_type and dev.dev_factory == dev_factory and dev.dev_model == dev_model:
                                new_exp = exp.replace(abs_cmd, act_cmd)
                                line = line.replace(exp, new_exp)
            str_script_translated += line
        return str_script_translated, agent_ip

def tc1():
    CmdSession.load_script('script.py')
    return

def tc2():
    CmdSession.translate_script('script.py')
    return

if __name__ == "__main__":
    tc2()