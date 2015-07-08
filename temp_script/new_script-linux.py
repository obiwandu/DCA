from dca_cmd import DcaCmd
from telnet_control import TestTelnetControl

dev1 = DcaCmd(TestTelnetControl, '10.137.59.22', 'tianyi.dty', 'Mtfbwy626488')

i = 2
for iter in range(i):
    dev1.execute('ls')
dev1.logout()