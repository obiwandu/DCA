from agent_invoker import AgentInvoker
from dca.dca_protocol import DcaProtocol

__author__ = 'User'

class AgentProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process(data):
        procedure_name, para, uuid = DcaProtocol.decap_input(data)
        result = AgentInvoker.invoke(procedure_name, para)
        feedback = DcaProtocol.encap_output(result, uuid)

        return feedback
