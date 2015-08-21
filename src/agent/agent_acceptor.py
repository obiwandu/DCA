from gevent.server import StreamServer

from agent_processor import AgentProcessor

__author__ = 'User'


class AgentAcceptor:
    """ Responsible for listening to request and respond to these hosts.
    """
    def __init__(self):
        pass

    @staticmethod
    def serve(port=8000):
        """ Start listening on the designated port

        Args:
            port: The port that current service listens on.

        Return:
            None. The request handler would send response directly to the host which starts the request.
        """
        print 'Service on port %s starts...' % port
        StreamServer(('', port), AgentAcceptor.accept).serve_forever()

    @staticmethod
    def accept(socket, address):
        """ Accept a request and pass the data to AgentProcessor.
        """
        data = socket.recv(4096)
        feedback = AgentProcessor.process(data)
        socket.sendall(feedback)
        return
