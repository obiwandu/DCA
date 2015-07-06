__author__ = 'User'

from new_template import TemplateNew
import re
import subprocess
from cmdline_interface import CmdLineInterface
from webapp_interface import WebAppInterface
from template import Template
from device_mngt import DeviceManagemnt
from datastructure import Command, Identity

class CmdSession:
    def __init__(self):
        return

    def exec_script(self):
        exec(open('script.py').read())

    @staticmethod
    def make_executable(cmd):
        return "master.exec_script_cmd('" + cmd + "')"

    @staticmethod
    def load_script(script_name):
        #find all keywords
        try:
            fp = open('template.xml', 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return

        abs_cmd = []
        temp_no = 1
        for line in fp:
            temp_no += 1
            command, identity, script = Template.parse_xml(line)
            abs_cmd.append(command.abs_cmd)

        #translate original script
        try:
            fp = open(script_name, 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return

        new_script_name = "new_" + script_name
        fout = open(new_script_name, 'w')

        line_no = 1
        for line in fp:
            line_no += 1
            for cmd in abs_cmd:
                if cmd in line:
                    new_cmd = CmdSession.make_executable(cmd)
                    line = line.replace(cmd, new_cmd)
            fout.write(line)

        return new_script_name

    @staticmethod
    def translate_script(script_name):
        # find all keywords
        try:
            fp = open('template.xml', 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return

        cmd = []
        temp_no = 1
        for line in fp:
            temp_no += 1
            command, identity, script = Template.parse_xml(line)
            cmd.append((command.abs_cmd, command.act_cmd, identity.dev_type, identity.dev_factory, identity.dev_model))

        #translate original script
        try:
            fp = open(script_name, 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return

        new_script_name = "new_" + script_name
        fout = open(new_script_name, 'w')

        device = dict()
        dev_mngt = DeviceManagemnt()
        for line in fp:
            if 'DcaCmd(' in line:
                var_name, exp = line.replace(' ', '').split('=')
                result = re.findall("'.*?'", exp)
                identity = Identity()
                identity.ip = result[0][1:-1]
                identity.dev_id = result[1][1:-1]
                identity.dev_pw = result[2][1:-1]
                dev_mngt.get_devinfo(identity)
                device[var_name] = identity

        fp = open(script_name, 'r')
        line_no = 1
        for line in fp:
            line_no += 1
            if 'execute' in line:
                # restriction: there must be space between operator and variables/methods.
                # This is coincident with standard of Python programming style
                for exp in line.split():
                    if 'execute' in exp:
                        var_name, method = exp.replace(' ','').split('.')
                        ident = device[var_name]
                        result = re.search("'.*?'", method).group()[1:-1]
                        for abs_cmd, act_cmd, dev_type, dev_factory, dev_model in cmd:
                            if abs_cmd == result and ident.dev_type == dev_type and ident.dev_factory == dev_factory and ident.dev_model == dev_model:
                                new_exp = exp.replace(abs_cmd, act_cmd)
                                line = line.replace(exp, new_exp)
            fout.write(line)
        return new_script_name

def tc1():
    CmdSession.load_script('script.py')
    return

def tc2():
    CmdSession.translate_script('script.py')
    return

if __name__ == "__main__":
    tc2()