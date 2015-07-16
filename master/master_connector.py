__author__ = 'User'
import socket
import gevent
from gevent import select
import Queue
import sys
from dca.dca_protocol import DcaProtocol

class MasterConnector:
    """ Handle data transmission and message listening.
    """
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.message_queue = dict()     # message_queue is used to store response from agent
        # if hasattr(select, 'epoll'):
        #     self._epoll = select.epoll()
        # elif hasattr(select, 'poll'):
        #     self._epoll = select.poll()
        # else:
        #     self.select = None

    def listen(self, request_dict):
        """ Listen to all sockets created by request in one co-routine. Receives data from them and check if all
            requests have been answered.
        """
        while True:
            gevent.sleep(1)   # switch to request co-routine
            # use select to get readable event
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0)

            if not (readable or writable or exceptional):
                print 'No input event'
                continue

            # polling readable event
            for s in readable:
                # data = s.recv(9999)
                buf = s.recv(9999)
                data = buf
                while len(buf):     # read until there's no data
                    buf = s.recv(9999)
                    data += buf
                if data:
                    # print 'recv data:', data, 'from', s.getpeername()
                    self.message_queue[s].put(data)     # put data into message_queue
                    self.inputs.remove(s)   # remove socket because only wait for one response
                    s.close()
                else:
                    # no data received
                    print 'close the connection', s.getpeername()
                    if s in self.outputs:
                        self.outputs.remove(s)
                    self.inputs.remove(s)
                    s.close()
                    del self.message_queue[s]

            # exceptional event
            for s in exceptional:
                print "exceptional connection:", s.getpeername()
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queue[s]

            # check if all requests have been answered
            if DcaProtocol.check_termination(self.message_queue, request_dict):
                print 'All requests have been answered'
                return request_dict
        return

    def request(self, data, ip):
        """ Send request to agent through tcp.
        """
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
                s.connect(sa)   # connect to remote host, here we only connect to agent
                s.setblocking(0)    # we use non-blocking socket
            except socket.error, msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print 'could not open socket'
            sys.exit(1)

        s.sendall(data)     # send data to agent

        # put socket into listening list which is waiting for response
        self.inputs.append(s)
        self.message_queue[s] = Queue.Queue()
        gevent.sleep(0.1)   # switch to listening handler

        # getting response and close socket would be done by listening handler
        return
