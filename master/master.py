from device.device_mngt import DeviceManagemnt
from util.template_handler import TemplateHandler
from dca.script_handler import ScriptHandler
from master_proxy import MasterProxy
import Queue
import uuid

class Master:
    """Provides public methods
    """
    def __init__(self):
        self.proxy = MasterProxy()
        self.message_queue = None
        self.listen = self.proxy.listen
        return

    # def listen(self):
    #     self.proxy.listen()
    #     self.message_queue = self.proxy.message_queue
    #     # traverse message_queue
    #     for key in self.message_queue:
    #         while not self.message_queue[key].empty():
    #             print self.message_queue[key].get()
    #
    #     # traverse requetst_queue
    #     while not self.request_queue.empty():
    #             print self.request_queue.get()

    def cfg_cmd(self, ip, command):
        """Configure command mapping and save the configuration as file.

        Stores command mapping between abstract and actual command in a file which could be used when translating
        command during remote execution.

        Args:
            ip: The ip address of target device.
            command: The data structure contains abstract command, actual command and a list of expecting result's field
                name and regex used to extract the result.

        Return:
            None.
        """
        agent_ip, dev_info = DeviceManagemnt.get_devinfo(ip)

        temphdl = TemplateHandler()
        temphdl.to_template(command, dev_info)
        return

    def exec_cmd(self, abs_cmd, identity, protocol):
        """Execute abstract directly on remote device.

        Args:
            abs_cmd: The abstract command that would be executed on remote device
            identity: The data structure contains device ip, id and password which could be used to log in the target
                device.
            protocol: The protocol class which defines the interaction methods from agent to device.

        Return:
            None. But the feedback of the execution would be stored in the message queue of current master object.
        """
        print 'Master: exec_cmd'
        # convert abs_cmd, identity to script
        str_script = ScriptHandler.generate_script(abs_cmd, identity, protocol)
        return self.proxy.remote_call('exec_script', str_script)

    def exec_script(self, script_name):
        """Execute script which is written by abstract command

        Args:
            script_name: The file name of script to be executed. The script directory is under script\ by default.

        Return:
            None. But the feedback of the execution would be stored in the message queue of current master object.
        """
        script_name = 'script\\%s' % script_name
        try:
            fp = open(script_name, 'r')
        except IOError, e:
            print 'Script file %s not found.' % e
            return
        str_script = fp.read()

        return self.proxy.remote_call('exec_script', str_script)
