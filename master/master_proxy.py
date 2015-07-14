from dca.script_handler import ScriptHandler
from master_invoker import MasterInvoker

__author__ = 'User'

class MasterProxy:
    """Handles mapping between device and agent.
    """
    def __init__(self):
        self.invoker = MasterInvoker()
        self.message_queue = None
        self.listen = self.invoker.listen
        pass

    # def listen(self):
    #     self.invoker.listen()
    #     self.message_queue = self.invoker.message_queue

    def remote_call(self, procedure_name, para):
        """Execute the remote call.

        Args:
            procedure_name: Name of the remote procedure.
            para: A short script contains one or more device ip, identity information and actual commands which could
                be executed on device.

        Return:
            None. But the feedback of the execution would be stored in the message queue of current master object.
        """
        print 'Proxy: remote_call'
        str_script, agent_ip = ScriptHandler.translate_script(para)
        return self.invoker.remote_call(procedure_name, str_script, agent_ip)

    # def get_result(self):
    #     return self.invoker.get_result()