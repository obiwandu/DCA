from agent_invoker import AgentInvoker
from dca.dca_protocol import DcaProtocol

__author__ = 'User'

class AgentProcessor:
    """ Parse and process the data from request.
    """
    def __init__(self):
        pass

    @staticmethod
    def process(data):
        """ Decapsulte data from request and pass them to AgentInvoker. Encapsulate the feedback.
        """
        procedure_name, para, uuid = DcaProtocol.decap_input(data)  # Decapsulate data into structured data
        result = AgentInvoker.invoke(procedure_name, para)  # pass these paras to AgentInvoker
        feedback = DcaProtocol.encap_output(result, uuid)   # Encapsulte the feedback

        return feedback
