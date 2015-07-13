__author__ = 'User'

class Agent:
    def __init__(self):
        pass

    @staticmethod
    def exec_cmd(script_path):
        result = dict()
        execfile(script_path, dict(), result)
        return result['script_ret']

    @staticmethod
    def exec_script(script_path):
        result = dict()
        execfile(script_path, dict(), result)
        return result['script_ret']
