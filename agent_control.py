__author__ = 'User'
from abc import ABCMeta, abstractmethod

class AgentControl:
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def login(self, identity):
        pass

    @abstractmethod
    def exec_cmd(self, command):
        pass

