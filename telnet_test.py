from telnetlib import Telnet
import getpass

# tn = Telnet("10.137.59.22")
# tn.write("vt100\n")
# print tn.read_until("login:")
# id = "tianyi.dty"
# tn.write(id + "\n")
# print tn.read_until("Password:")
# pw = "Mtfbwy626488"
# tn.write(pw + "\n")
# print tn.read_until("~]$")
# tn.write("ll\n")
# tn.write("exit\n")
# print tn.read_until("~]$")

# pw = getpass.getpass()
pw = "Mtfbwy626488"
print pw
tn = Telnet("10.137.59.22")
tn.read_until("login: ")
tn.write("tianyi.dty" + "\n")
tn.read_until("Password: ")
tn.write(pw + "\n")
tn.write("ll\n")
tn.write("exit\n")
print tn.read_all()
