__author__ = 'User'

from datastructure import Command
from datastructure import Identity
from template import Template

def tc1():
    command = Command()
    identity = Identity()
    command.abs_cmd = 'show'
    command.act_cmd = 'show -hw'
    command.exp_result.append(('output','\d'))
    command.exp_result.append(('extra_info','\w'))
    identity.ip = '1.1.1.1'
    identity.dev_id = 'root'
    identity.dev_pw = '123456'
    identity.dev_type = 'switch'
    identity.dev_factory = 'HW'
    identity.dev_model = '150'
    # print Template.to_xml(command)
    print Template.to_xml(command, identity)

def tc2():
    str_xml1 = '<template><command><abs_cmd>show</abs_cmd><act_cmd>show -hw</act_cmd><exp_result><output>\d</output><extra_info>\w</extra_info></exp_result></command></template>'
    str_xml2 = '<template><command><abs_cmd>show</abs_cmd><act_cmd>show -hw</act_cmd><exp_result><output>\d</output><extra_info>\w</extra_info></exp_result></command><identity><ip>1.1.1.1</ip><dev_id>root</dev_id><dev_pw>123456</dev_pw><dev_type>switch</dev_type><dev_factory>HW</dev_factory><dev_model>150</dev_model></identity></template>'
    command = Command()
    identity = Identity()
    command, identity = Template.parse_xml(str_xml1)
    command.show()
    identity.show()
    command, identity = Template.parse_xml(str_xml2)
    command.show()
    identity.show()

def tc3():
    template = Template()
    command = Command()
    identity = Identity()
    command.abs_cmd = 'show'
    command.act_cmd = 'show -hw'
    command.exp_result.append(('output','\d'))
    command.exp_result.append(('extra_info','\w'))
    identity.ip = '1.1.1.1'
    identity.dev_id = 'root'
    identity.dev_pw = '123456'
    identity.dev_type = 'switch'
    identity.dev_factory = 'HW'
    identity.dev_model = '150'
    template.to_template(command, identity)

def tc4():
    template = Template()
    ident = Identity()
    ident.dev_factory = 'HW'
    ident.dev_type = 'switch'
    ident.dev_model = '150'
    print template.find('show', ident)

if __name__ == "__main__":
    # testcase_gen_xml()
    tc4()
