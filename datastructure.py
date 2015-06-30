__author__ = 'User'

class Identity:
    def __init__(self):
        self.ip = None
        self.dev_id = None
        self.dev_pw = None
        self.dev_factory = None
        self.dev_type = None
        self.dev_model = None
        return

    def show(self):
        print 'ip:', self.ip
        print 'dev_id:', self.dev_id
        print 'dev_pw:', self.dev_pw
        print 'dev_factory:', self.dev_factory
        print 'dev_type:', self.dev_type
        print 'dev_model:', self.dev_model

class Command:
    def __init__(self):
        self.abs_cmd = None
        self.act_cmd = None
        self.exp_result = []
        return

    def show(self):
        print 'abs_cmd:', self.abs_cmd
        print 'act_cmd:', self.act_cmd
        print 'exp_result:'
        for field in self.exp_result:
            print '    ', field