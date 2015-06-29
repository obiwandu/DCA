__author__ = 'User'
from abc import ABCMeta, abstractmethod

class MasterInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def login(self, identity):
        pass

    @abstractmethod
    def cfg_cmd(self, command):
        pass

    @abstractmethod
    def exec_script(self, script_name):
        pass