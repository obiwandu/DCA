__author__ = 'User'

from new_template import TemplateNew
import re
import subprocess
from cmdline_interface import CmdLineInterface
from webapp_interface import WebAppInterface
from template import Template

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
            # print 'template %s:' % temp_no, line
            temp_no += 1
            command, identity = Template.parse_xml(line)
            # cmd, exp_res, exec_para = TemplateNew.parse_xml(line)
            abs_cmd.append(command.abs_cmd)
            # abs_cmd.append(cmd['abs_cmd'])

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
            # print "line %s" % line_no, line
            line_no += 1
            for cmd in abs_cmd:
                # new_cmd = cmd + 'exec'
                if cmd in line:
                    new_cmd = CmdSession.make_executable(cmd)
                    line = line.replace(cmd, new_cmd)
            fout.write(line)

        # with open("out.txt", "wt") as fout:
        #     with open("Stud.txt", "rt") as fin:
        #         for line in fin:
        #             fout.write(line.replace('A', 'Orange'))
        return new_script_name

def tc1():
    CmdSession.load_script()
    return

if __name__ == "__main__":
    tc1()