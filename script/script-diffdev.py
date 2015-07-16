from dca.dca_cmd import DcaCmd
from control_protocol.telnet_stub_control import TelnetStubControl

dev1 = DcaCmd(TelnetStubControl, '1.1.1.1', 'root', '123456')   # initialize an instance to operate 1.1.1.1
dev2 = DcaCmd(TelnetStubControl, '192.168.0.1', 'admin', 'hello')   # initialize an instance to operate 192.168.0.1
i = 2
for iter in range(i):
    if dev1.execute('show') == dev2.execute('show'):    # execute abstract command
        script_ret = dev1.execute('ps')  # execute abstract command
dev1.logout()   # disconnect from 1.1.1.1
dev2.logout()   # disconnect from 192.168.0.1
