import re
from dca.dca_cmd import DcaCmd
from control_protocol.ssh_server_control import SSHServerControl

dev1 = DcaCmd(SSHServerControl, '10.137.59.22', 'tianyi.dty', 'Mtfbwy626488')   # initialize an instance to operate 10.137.59.22
dev2 = DcaCmd(SSHServerControl, '10.65.7.131', 'root', 'hello1234') # initialize an instance to operate 10.65.7.131

feedback1 = dev1.execute('hwinfo')  # execute abstract command
feedback2 = dev2.execute('hwinfo')  # execute abstract command
cpu_number_dev1 = re.search('CPU\(s\): *\d+', feedback1).group().split()[1]  # parse result from feedback
cpu_number_dev2 = re.search('CPU\(s\): *\d+', feedback2).group().split()[1]  # parse result from feedback

# cpu_number_dev2 = re.search('', dev2.execute('hwinfo'))
if cpu_number_dev1 == cpu_number_dev2:
    script_ret = dev2.execute('networkinfo')    # execute abstract command

dev1.logout()   # disconnect from 10.137.59.22
dev2.logout()   # disconnect from 10.65.7.131
