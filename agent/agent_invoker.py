from agent import Agent
import os

__author__ = 'User'

class AgentInvoker:
    def __init__(self):
        pass

    @staticmethod
    def invoke(procedure_name, para):
        if procedure_name == 'exec_cmd':
            script_path = 'temp_script.py'
            fp = open(script_path, 'w')
            fp.write(para)
            fp.close()
            feedback = Agent.exec_cmd(script_path)
            os.remove(script_path)
        elif procedure_name == 'exec_script':
            script_path = 'temp_script.py'
            fp = open(script_path, 'w')
            fp.write(para)
            fp.close()
            feedback = Agent.exec_script(script_path)
            os.remove(script_path)
        else:
            feedback = 'Invalid command, not handled'

        return feedback
