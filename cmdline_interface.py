__author__ = 'User'

from master_interface import MasterInterface
from datastructure import Command
from datastructure import Identity
import getpass

class CmdLineInterface(MasterInterface):
    def login(self, identity):
        #just for test
        identity.ip =  '10.137.59.22'
        identity.dev_id = 'tianyi.dty'
        identity.dev_pw = 'Mtfbwy626488'
        # identity.ip = raw_input("Input the IP address:")
        # identity.dev_id = raw_input("Input the device user id:")
        # identity.dev_pw = getpass.getpass()
        return

    def cfg_cmd(self, command):
        command.abs_cmd = raw_input("Input the abstract command:")
        command.act_cmd = raw_input("Input the actual command:")
        result_cnt = raw_input("Input the number of result field:")
        for i in range(int(result_cnt)):
            key = raw_input("Input the key of result:")
            val = raw_input("Input the regular expression of result:")
            command.exp_result.append((key, val))
        return

    def exec_cmd(self):
        return raw_input("Input the abstract command:")

    def exec_script(self):
        return raw_input('Input the script to be executed:')