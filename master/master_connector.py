__author__ = 'User'
import socket
import gevent
from gevent import select
import Queue
import sys
from dca.dca_protocol import DcaProtocol

class MasterConnector:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.message_queue = dict()
        # if hasattr(select, 'epoll'):
        #     self._epoll = select.epoll()
        # elif hasattr(select, 'poll'):
        #     self._epoll = select.poll()
        # else:
        #     self.select = None

    def listen(self, request_dict):
        print 'Connector: listen'
        while True:
            gevent.sleep(1)
            # print 'waiting for connection'
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0)

            if not (readable or writable or exceptional):
                print 'No input event'
                continue

            # polling readable event
            for s in readable:
                # type of s should be checked here
                # if s is socket.socket.fileno:
                    # data from server
                data = s.recv(1024)
                if data:
                    print 'recv data:', data, 'from', s.getpeername()
                    self.message_queue[s].put(data)
                    self.inputs.remove(s)
                    s.close()
                else:
                    print 'close the connection', s.getpeername()
                    if s in self.outputs:
                        self.outputs.remove(s)
                    self.inputs.remove(s)
                    s.close()
                    del self.message_queue[s]

            for s in exceptional:
                print "exceptional connection:", s.getpeername()
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queue[s]

            if DcaProtocol.check_termination(self.message_queue, request_dict):
                print 'All requests have been answered'
                return
        return

    def request(self, data, ip):
        print 'Connector: request'
        port = 8000
        s = None
        for res in socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error, msg:
                s = None
                continue
            try:
                s.connect(sa)
                s.setblocking(0)
            except socket.error, msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print 'could not open socket'
            sys.exit(1)

        # send data to agent
        s.sendall(data)

        # put socket which is waiting for recv here
        self.inputs.append(s)
        self.message_queue[s] = Queue.Queue()
        gevent.sleep(0.1)
        # recv and close would be done by handler
        return
