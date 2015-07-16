from master_connector import MasterConnector
from dca.dca_protocol import DcaProtocol
import uuid

__author__ = 'User'

class MasterInvoker:
    """ Responsible for call communication interface to send data or start listening.
    """
    def __init__(self):
        self.connector = MasterConnector()
        self.request_dict = dict()
        pass

    def listen(self):
        """ Start listening.
        """
        return self.connector.listen(self.request_dict)

    def remote_call(self, procedure_name, para, ip):
        """ Encapsulte the data and call the Connector to send the request.
        """
        id = uuid.uuid4()   # generate a uuid for every request
        data = DcaProtocol.encap_input(procedure_name, para, id)

        self.request_dict[id] = False  # initialized a dict to indicate if a request is answered
        self.connector.request(data, ip)
        return id
