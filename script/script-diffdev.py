from dca.dca_cmd import DcaCmd
from control_protocol.telnet_stub_control import TelnetStubControl

dev1 = DcaCmd(TelnetStubControl, '1.1.1.1', 'root', '123456')
dev2 = DcaCmd(TelnetStubControl, '192.168.0.1', 'admin', 'hello')
i = 2
for iter in range(i):
    if dev1.execute('show') == dev2.execute('show'):
        script_ret = dev1.execute('ps')
dev1.logout()
dev2.logout()
