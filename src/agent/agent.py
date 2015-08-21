__author__ = 'User'

class Agent:
    """ Where the remote procedures exist.
    """
    def __init__(self):
        pass

    @staticmethod
    def exec_cmd(script_path):
        """ Execute a single command from master.
        """
        # we don't use this method for now.
        result = dict()
        execfile(script_path, dict(), result)
        return result['script_ret']

    @staticmethod
    def exec_script(script_path):
        """ Execute a script from master.
        """
        result = dict()
        execfile(script_path, dict(), result)
        return result['script_ret']
