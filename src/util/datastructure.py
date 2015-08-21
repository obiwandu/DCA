__author__ = 'User'

class Identity:
    """ Data structure of identity information
    """
    def __init__(self):
        self.ip = None  # string of device ip address
        self.dev_id = None  # string of device id
        self.dev_pw = None  # string of device password
        return

    def show(self):
        print 'ip:', self.ip
        print 'dev_id:', self.dev_id
        print 'dev_pw:', self.dev_pw

class DevInfo:
    """ Data structure of device information
    """
    def __init__(self):
        self.dev_factory = None     # string of device vendor
        self.dev_type = None    # string of device type
        self.dev_model = None   # string of device model
        return

    def show(self):
        print 'dev_factory', self.dev_factory
        print 'dev_type', self.dev_type
        print 'dev_model', self.dev_model

class Command:
    """ Data structure of command
    """
    def __init__(self):
        self.abs_cmd = None     # string of abstract command
        self.act_cmd = None     # string of actual command
        self.exp_result = []    # list of expected result. Every item is a tuple which contains a name of result and a regex
        return

    def show(self):
        print 'abs_cmd:', self.abs_cmd
        print 'act_cmd:', self.act_cmd
        print 'exp_result:'
        for field in self.exp_result:
            print '    ', field
