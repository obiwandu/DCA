import gevent

from datastructure import Identity, Command
from master.master import Master
from control_protocol.telnet_control import TestTelnetControl

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

    listen = gevent.spawn(master.listen)
    req = gevent.spawn(Master.exec_script, 'script-diffdev.py')
    req1 = gevent.spawn(Master.exec_script, 'script-diffdev.py')
    req2 = gevent.spawn(Master.exec_script, 'script-diffdev.py')

    # req3 = gevent.spawn(Master.exec_script, 'script-diffdev.py')

    identity = Identity()
    identity.ip = '10.137.59.22'
    identity.dev_id = 'tianyi.dty'
    identity.dev_pw = 'Mtfbwy626488'
    req3 = gevent.spawn(Master.exec_cmd('dir', identity, TestTelnetControl))

    gevent.joinall([listen, req, req1, req2, req3])
