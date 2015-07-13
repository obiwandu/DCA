from dca.dca_cmd import DcaCmd
from control_protocol.telnet_control import TestScriptControl

dev1 = DcaCmd(TestScriptControl, '1.1.1.1', 'root', '123456')
dev2 = DcaCmd(TestScriptControl, '192.168.0.1', 'admin', 'hello')
i = 2
for iter in range(i):
    if dev1.execute('show -hw') == dev2.execute('show -cisco'):
        script_ret = dev1.execute('ps -hw')
dev1.logout()
dev2.logout()
