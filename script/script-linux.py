import re
from dca.dca_cmd import DcaCmd
from control_protocol.ssh_server_control import SSHServerControl

dev1 = DcaCmd(SSHServerControl, '10.137.59.22', 'tianyi.dty', 'Mtfbwy626488')
dev2 = DcaCmd(SSHServerControl, '10.65.7.131', 'root', 'hello1234')

feedback1 = dev1.execute('hwinfo')
feedback2 = dev2.execute('hwinfo')
cpu_number_dev1 = re.search('CPU\(s\): *\d+', feedback1).group().split()[1]
cpu_number_dev2 = re.search('CPU\(s\): *\d+', feedback2).group().split()[1]

# cpu_number_dev2 = re.search('', dev2.execute('hwinfo'))
if cpu_number_dev1 == cpu_number_dev2:
    script_ret = dev2.execute('networkinfo')

dev1.logout()
dev2.logout()