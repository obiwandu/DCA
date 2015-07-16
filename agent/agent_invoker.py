from agent import Agent
import os

__author__ = 'User'

class AgentInvoker:
    """ Execute the calling of remote procedure.
    """
    def __init__(self):
        pass

    @staticmethod
    def invoke(procedure_name, para):
        """ Call the actual procedure that the request needs to call.
        """
        # now we use the same way to deal with command and script
        if procedure_name == 'exec_cmd' or procedure_name == 'exec_script':
            script_path = 'temp_script.py'
            fp = open(script_path, 'w')     # write script to a script file
            fp.write(para)
            fp.close()
            feedback = Agent.exec_script(script_path)   # execute the script file
            os.remove(script_path)
        else:
            feedback = 'Invalid command, not handled'

        return feedback
