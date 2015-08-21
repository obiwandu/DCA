__author__ = 'User'

import re

from util.template_handler import TemplateHandler
from device.device_mngt import DeviceManagemnt
from util.datastructure import Identity


class ScriptHandler:
    """ Handle generation and translation of script according to local command template.
    """
    def __init__(self):
        return

    @staticmethod
    def generate_script(abs_cmd, identity, protocol):
        """ Generate a simple script according to existing abstract command, identity information and protocol information.
        """
        # a script template for script generation
        script_template = "from dca.dca_cmd import DcaCmd\n" \
                   "from control_protocol.{module_name} import {class_name}\n" \
                   "dev1 = DcaCmd({class_name}, '{ip}', '{dev_id}', '{dev_pw}')\n" \
                   "script_ret = dev1.execute('{cmd}')\n" \
                   "dev1.logout()"
        # replace these elements by specified parameters
        script = script_template.format(module_name=protocol[0], class_name=protocol[1], ip=identity.ip, \
                                        dev_id=identity.dev_id, dev_pw=identity.dev_pw, cmd=abs_cmd)
        return script

    @staticmethod
    def translate_script(str_script):
        """ Translate a script which contains abstract command into an executable script on real device according to local
            command template configured by user.
        """
        # load all configurations into a list
        try:
            fp = open('template\\template.xml', 'r')
        except IOError, e:
            print 'File %s not found.' % e
            return
        cmd = []
        temp_no = 1
        for line in fp:
            temp_no += 1
            command, dev_info = TemplateHandler.parse_template(line)    # parse xml into structured data
            cmd.append((command.abs_cmd, command.act_cmd, dev_info.dev_type, dev_info.dev_factory, dev_info.dev_model))

        # parse original script to get identity information
        str_script_translated = ''
        device = dict()
        agent_ip = None
        script_line = str_script.split('\n')    # handle the script by line
        for line in script_line:
            if 'DcaCmd(' in line:   # find initialization of DcaCmd object where the identity info exists
                var_name, exp = line.replace(' ', '').split('=')    # get name and para of DcaCmd object
                result = re.findall("'.*?'", exp)
                identity = Identity()
                identity.ip = result[0][1:-1]
                identity.dev_id = result[1][1:-1]
                identity.dev_pw = result[2][1:-1]
                temp_agent_ip, dev_info = DeviceManagemnt.get_devinfo(identity.ip)  # get agent ip and device info from device ip
                if not agent_ip:
                    agent_ip = temp_agent_ip
                else:
                    if temp_agent_ip != agent_ip:   # this indicates current device doesn't belong to the same agent with the previous device
                        print "devices don't belong to one unique agent"
                        return
                device[var_name] = dev_info     # associate device info with the object name

        # start translation
        line_no = 1
        for line in script_line:
            line_no += 1
            if '#' in line:     # escape comment
                line = line[:line.index('#')]
            if 'execute' in line:   # locate the abstract command
                # restriction: there must be space between operator and variables/methods.
                # This is coincident with standard of Python programming style
                for exp in line.split():
                    if 'execute' in exp:
                        var_name, method = exp.replace(' ', '').split('.')  # extract object name and method
                        dev = device[var_name]
                        result = re.search("'.*?'", method).group()[1:-1]   # extract abstract command
                        for abs_cmd, act_cmd, dev_type, dev_factory, dev_model in cmd:  # search in local template
                            # whether current abstract command fits current item in template file
                            if abs_cmd == result and dev.dev_type == dev_type and dev.dev_factory == dev_factory and dev.dev_model == dev_model:
                                new_exp = exp.replace(abs_cmd, act_cmd)     # replace abstract command with actual comamnd
                                line = line.replace(exp, new_exp)       # replace original expression with new expression
                                break
            str_script_translated += line + '\n'
        return str_script_translated, agent_ip
