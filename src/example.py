from master.master import Master
from util.datastructure import Command, Identity

__author__ = 'User'

def tutorial_cfg_cmd():
    """ Configure some command templates.
    """
    master = Master()
    cmd = Command()
    cmd.abs_cmd = 'hwinfo'
    cmd.act_cmd = 'lscpu'
    master.cfg_cmd('10.65.7.131', cmd)
    cmd.abs_cmd = 'hwinfo'
    cmd.act_cmd = 'lscpu'
    master.cfg_cmd('10.137.59.22', cmd)
    cmd.abs_cmd = 'networkinfo'
    cmd.act_cmd = 'ifconfig'
    master.cfg_cmd('10.65.7.131', cmd)
    cmd.abs_cmd = 'networkinfo'
    cmd.act_cmd = 'ifconfig'
    master.cfg_cmd('10.137.59.22', cmd)

def tutorial_exec_script():
    """ Configure two types of comamands, then execute a script to show hardware and network information on device
        (here we use linux server instead of real device)
    """
    master = Master()
    cmd = Command()

    cmd.abs_cmd = 'hwinfo'
    cmd.act_cmd = 'lscpu'
    master.cfg_cmd('10.65.7.131', cmd)
    cmd.abs_cmd = 'hwinfo'
    cmd.act_cmd = 'lscpu'
    master.cfg_cmd('10.137.59.22', cmd)
    cmd.abs_cmd = 'networkinfo'
    cmd.act_cmd = 'ifconfig'
    master.cfg_cmd('10.65.7.131', cmd)

    para_list = [('script', 'script-linux.py')]
    result = master.execute(para_list)
    print 'result:'
    print result

def tutorial_exec_cmd():
    """ Configure one command and execute it to show network interface information on device(here we use linux server
        instead of real device)
    """
    master = Master()
    cmd = Command()

    cmd.abs_cmd = 'networkinfo'
    cmd.act_cmd = 'ifconfig'
    master.cfg_cmd('10.137.59.22', cmd)

    para_list = []
    identity1 = Identity()
    identity1.ip = '10.137.59.22'
    identity1.dev_id = 'tianyi.dty'
    identity1.dev_pw = 'Mtfbwy626488'
    telnetPro = ('telnet_server_control', 'TelnetServerControl')
    para_list.append(('cmd', 'networkinfo', identity1, telnetPro))
    result = master.execute(para_list)
    print 'result:'
    print result

# Contains same abstract commands on different devices
def tutorial_exec_script2():
    """ Configure two commands which have the same abstract command on different devices. Then execute a script which
        contains both these commands to show network interface information on device(here we use linux server instead
        of real device)
    """
    master = Master()
    cmd = Command()

    cmd.abs_cmd = 'show'
    cmd.act_cmd = 'show -hw'
    master.cfg_cmd('1.1.1.1', cmd)
    cmd.abs_cmd = 'ps'
    cmd.act_cmd = 'ps -hw'
    master.cfg_cmd('1.1.1.1', cmd)
    cmd.abs_cmd = 'show'
    cmd.act_cmd = 'show -cisco'
    master.cfg_cmd('192.168.0.1', cmd)

    para_list = [('script', 'script-diffdev.py')]
    result = master.execute(para_list)
    print 'result:'
    print result