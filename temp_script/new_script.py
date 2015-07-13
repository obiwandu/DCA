from dca.dca_cmd import DcaCmd
from telnet_control import TestScriptControl

dca = DcaCmd(TestScriptControl, '1.1.1.1', 'root', '123456')
temp = DcaCmd(TestScriptControl, '192.168.0.1', 'admin', 'hello')
i = 2
for iter in range(i):
    if dca.execute('show -hw') == temp.execute('show -cisco'):
        script_ret = dca.execute('ps -hw')
dca.logout()
