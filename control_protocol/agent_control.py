__author__ = 'User'
from abc import ABCMeta, abstractmethod

class AgentControl:
    """ An abstract class which is the base class of all other protocol control classes. Define some basic operations.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def login(self, identity):
        pass

    @abstractmethod
    def exec_cmd(self, command):
        pass

    @abstractmethod
    def logout(self):
        pass