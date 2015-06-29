__author__ = 'User'


class Identity:
    def __init__(self):
        self.ip = None
        self.dev_id = None
        self.dev_pw = None
        self.factory = None
        self.model = None
        return

class Command:
    def __init__(self):
        self.abs_cmd = None
        self.act_cmd = None
        self.exp_res = []
        return
