import gevent

from util.datastructure import Identity
from master.master import Master

__author__ = 'User'

if __name__ == "__main__":
    master = Master()

    # cmd = Command()
    # cmd.abs_cmd = 'dir'
    # cmd.act_cmd = 'ls'
    # master.cfg_cmd('1.1.1.1', cmd)
    # cmd.abs_cmd = 'show'
    # cmd.act_cmd = 'show -hw'
    # master.cfg_cmd('1.1.1.1', cmd)
    # cmd.abs_cmd = 'show'
    # cmd.act_cmd = 'show -cisco'
    # master.cfg_cmd('192.168.0.1', cmd)

    # listen = gevent.spawn(master.listen)
    # req = gevent.spawn(master.exec_script, 'script-diffdev.py')
    # req1 = gevent.spawn(master.exec_script, 'script-diffdev.py')
    # req2 = gevent.spawn(master.exec_script, 'script-diffdev.py')

    # req3 = gevent.spawn(master.exec_script, 'script-diffdev.py')

    identity = Identity()
    identity.ip = '10.137.59.22'
    identity.dev_id = 'tianyi.dty'
    identity.dev_pw = 'Mtfbwy626488'
    # req3 = gevent.spawn(master.exec_cmd, 'dir', identity, ('telnet_server_control', 'TelnetServerControl'))

    # gevent.joinall([listen, req, req1, req2, req3])
    # gevent.joinall([listen, req3])

    # print 'req ret:', req.value
    # print 'req1 ret:', req1.value
    # print 'req2 ret:', req2.value
    # print 'req3 ret:', req3.value

    para_list = []
    identity1 = Identity()
    identity1.ip = '10.137.59.22'
    identity1.dev_id = 'tianyi.dty'
    identity1.dev_pw = 'Mtfbwy626488'
    telnetPro = ('telnet_server_control', 'TelnetServerControl')
    para_list.append(('script', 'script-diffdev.py'))
    para_list.append(('cmd', 'dir', identity1, telnetPro))
    result = master.execute(para_list)
    print 'result:'
    print result
