import gevent

from master_connector import MasterConnector
from dca.dca_protocol import DcaProtocol

__author__ = 'User'

class MasterInvoker:
    def __init__(self):
        self.connector = MasterConnector()
        self.listen = self.connector.listen
        pass

    @staticmethod
    def remote_call(procedure_name, para, ip):
        data = DcaProtocol.encap(procedure_name, para)

        conn = MasterConnector()
        request = gevent.spawn(conn.request, data, ip)
        listen = gevent.spawn(conn.listen)
        gevent.joinall([request, listen])
        return