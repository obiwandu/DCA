from master_connector import MasterConnector
from dca.dca_protocol import DcaProtocol
import uuid

__author__ = 'User'

class MasterInvoker:
    def __init__(self):
        self.connector = MasterConnector()
        self.message_queue = None
        self.request_dict = dict()
        pass

    def listen(self):
        print 'Invoker: listen'
        self.connector.listen(self.request_dict)

    def remote_call(self, procedure_name, para, ip):
        print 'Invoker: remote_call'
        id = uuid.uuid4()
        data = DcaProtocol.encap_input(procedure_name, para, id)

        self.request_dict[id] = False  # initialized but empty
        self.connector.request(data, ip)
        return id

    # def get_result(self):
    #     while not self.message_queue.empty():
    #         result = self.message_queue.get()
    #         feedback, id = DcaProtocol.decap_output(result)
    #         self.result[id] = feedback
    #     return self.result