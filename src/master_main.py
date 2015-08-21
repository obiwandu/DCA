import gevent

from util.datastructure import Identity, Command
from master.master import Master

from example import *

__author__ = 'User'

if __name__ == "__main__":
    tutorial_cfg_cmd()
    tutorial_exec_script()
    tutorial_exec_cmd()
    tutorial_exec_script2()