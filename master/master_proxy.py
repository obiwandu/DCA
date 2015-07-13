from dca.script_handler import ScriptHandler
from master_invoker import MasterInvoker

__author__ = 'User'

class MasterProxy:
    def __init__(self):
        self.invoker = MasterInvoker()
        self.listen = self.invoker.listen
        pass

    @staticmethod
    def remote_call(procedure_name, para):
        str_script, agent_ip = ScriptHandler.translate_script(para)
        MasterInvoker.remote_call(procedure_name, str_script, agent_ip)
        return
