from dca.dca_cmd import DcaCmd
from control_protocol.telnet_stub_control import TelnetStubControl

dev1 = DcaCmd(TelnetStubControl, '10.137.59.22', 'tianyi.dty', 'Mtfbwy626488')

i = 2
for iter in range(i):
    dev1.execute('dir')
dev1.logout()