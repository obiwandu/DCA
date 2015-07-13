from agent_invoker import AgentInvoker
from dca.dca_protocol import DcaProtocol

__author__ = 'User'

class AgentProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process(data):
        procedure_name, para = DcaProtocol.decap(data)
        feedback = AgentInvoker.invoke(procedure_name, para)
        return feedback
