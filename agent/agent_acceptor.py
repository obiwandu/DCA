from gevent.server import StreamServer

from agent_processor import AgentProcessor

__author__ = 'User'


class AgentAcceptor:
    def __init__(self):
        pass

    @staticmethod
    def serve(port):
        print 'Serving on 8000 starts...'
        server = StreamServer(('', 8000), AgentAcceptor.accept).serve_forever()

    @staticmethod
    def accept(socket, address):
        data = socket.recv(4096)
        feedback = AgentProcessor.process(data)
        socket.sendall(feedback)
        return
