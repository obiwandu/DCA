from device_mngt import DeviceManagemnt
from template_handler import TemplateHandler
from script_handler import ScriptHandler
from master_proxy import MasterProxy


class Master:
    def __init__(self):
        # init the input interface
        self.proxy = MasterProxy()
        self.listen = self.proxy.listen
        return

    @staticmethod
    def cfg_cmd(ip, command):
        agent_ip, dev_info = DeviceManagemnt.get_devinfo(ip)

        temphdl = TemplateHandler()
        temphdl.to_template(command, dev_info)
        return

    @staticmethod
    def exec_cmd(abs_cmd, identity, protocol):
        # convert abs_cmd, identity to script
        str_script = ScriptHandler.generate_script(abs_cmd, identity, protocol)
        MasterProxy.remote_call('exec_cmd', str_script)
        return

    @staticmethod
    def exec_script(script_name):
        script_name = 'script\\%s' % script_name
        try:
            fp = open(script_name, 'r')
        except IOError, e:
            print 'Script file %s not found.' % e
            return
        str_script = fp.read()

        MasterProxy.remote_call('exec_script', str_script)
        return


