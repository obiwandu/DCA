from gevent.server import StreamServer

__author__ = 'User'

def application(socket, address):
    print('New connection from %s:%s' % address)
    # socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    data = socket.recv(1024)
    print data
    socket.sendall('data recved')
    # rfileobj = socket.makefile(mode='rb')
    # line = rfileobj.readline()
    # while line:
    #     line = rfileobj.readline()
    #     if not line:
    #         print("client disconnected")
    #         break
    #     else:
    #         print line
    #     # if line.strip().lower() == b'quit':
    #     #     print("client quit")
    #     #     break
    #     socket.sendall(line)
    #     print("echoed %r" % line)
    # rfileobj.close()
    return


    # code = '200 OK'
    # msg = 'SUCCESS'
    # success = True
    #
    # print "new msg arrives"
    # print env
    # handler = Handler(env, TestTelnetControl)
    # msg = handler.msg_executor()
    # start_response(code, [('Content-Type', 'text/plain')])
    #
    # return ['%s\n' % str(msg)]

if __name__ == "__main__":
    print 'Serving on 8000 starts...'
    server = StreamServer(('127.0.0.1', 8000), application).serve_forever()
