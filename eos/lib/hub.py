#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by lingjiao.lc

"""
Note, in my script, a tab equals four blanks.
You must have a check of your indentation.
"""

import os
import sys
import logging
from eos import exceptions
from eos import log

HUB_TYPE = os.getenv('eos_HUB_TYPE', 'eventlet')

log.setup_logging('eos.lib.hub', 'lib.log')
LOG = logging.getLogger('eos.lib.hub')

if HUB_TYPE == 'eventlet':
    import eventlet
    import eventlet.event
    import eventlet.queue
    import eventlet.timeout
    import eventlet.wsgi
    import greenlet
    import ssl
    import socket
    import traceback

    getcurrent = eventlet.getcurrent
    patch = eventlet.monkey_patch
    sleep = eventlet.sleep

    def spawn(*args, **kwargs):
        def _launch(func, *args, **kwargs):
            # mimic gevent's default raise_error=False behaviour
            # by not propergating an exception to the joiner.
            try:
                func(*args, **kwargs)
            except greenlet.GreenletExit, e:
                raise e
            except:
                # log uncaught exception.
                # note: this is an intentional divergence from gevent
                # behaviour.  gevent silently ignores such exceptions.
                LOG.error('hub: uncaught exception: %s',
                          traceback.format_exc())

        return eventlet.spawn(_launch, *args, **kwargs)

    def kill(thread):
        thread.kill()

    def joinall(threads):
        for t in threads:
            # this try-except is necessary when killing an inactive
            # greenthread
            try:
                t.wait()
            except greenlet.GreenletExit:
                pass

    Queue = eventlet.queue.Queue
    QueueEmpty = eventlet.queue.Empty
    
    class work_map(object):             
        def __init__(self, size=0):
            self.size = size
            self.d = {}
        
        def put(self, name, o):
            if self.size != 0 and self.len() < self.size:
                self.d[name] = o
            elif self.size == 0:
                self.d[name] = o
            else:
                raise exceptions.mapFull()
            
        def get(self, name):
            return self.d.get(name, None)
        
        def pop(self, name):
            self.d.pop(name, 0)
            
        
        def full(self):
            if self.size == 0:
                return False
            else:
                return self.len() >= self.size
            
        def len(self):
            return len(self.d.items())
            
        def empty(self):
            return True if self.len() == 0 else False
            
    class StreamServer(object):
        def __init__(self, listen_info, handle=None, backlog=None,
                     spawn='default', **ssl_args):
            assert backlog is None
            assert spawn == 'default'

            if ':' in listen_info[0]:
                self.server = eventlet.listen(listen_info,
                                              family=socket.AF_INET6)
            else:
                self.server = eventlet.listen(listen_info)
            if ssl_args:
                def wrap_and_handle(sock, addr):
                    ssl_args.setdefault('server_side', True)
                    handle(ssl.wrap_socket(sock, **ssl_args), addr)

                self.handle = wrap_and_handle
            else:
                self.handle = handle

        def serve_forever(self):
            while True:
                sock, addr = self.server.accept()
                spawn(self.handle, sock, addr)
    
    """
    当心里的负担七七八八卸的差不多的时候，我会认真地考虑去开肉夹馍店。闲暇时候操起老本行玩玩开发板。
    """

    class WSGIServer(StreamServer):
        def serve_forever(self):
            self.serve = eventlet.wsgi.server(self.server, self.handle)

    Timeout = eventlet.timeout.Timeout

    class Event(object):
        def __init__(self):
            self._ev = eventlet.event.Event()
            self._cond = False

        def _wait(self, timeout=None):
            while not self._cond:
                self._ev.wait()

        def _broadcast(self):
            self._ev.send()
            # because eventlet Event doesn't allow mutiple send() on an event,
            # re-create the underlying event.
            # note: _ev.reset() is obsolete.
            self._ev = eventlet.event.Event()

        def set(self):
            self._cond = True
            self._broadcast()

        def clear(self):
            self._cond = False

        def wait(self, timeout=None):
            if timeout is None:
                self._wait()
            else:
                try:
                    with Timeout(timeout):
                        self._wait()
                except Timeout:
                    pass

            return self._cond



if __name__ == "__main__":
    pass

