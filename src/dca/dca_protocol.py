from xml.etree import ElementTree
import uuid
__author__ = 'User'

class DcaProtocol:
    """ Include encapsulation and decapsulation of data between master and agent.
    """
    def __init__(self):
        pass

    @staticmethod
    def encap_input(procedure_name, para, id):
        """ Encapsulate data into xml string when master sends request.
        """
        root = ElementTree.Element('Procedure')
        element = ElementTree.SubElement(root, 'UUID')
        element.text = str(id)
        element = ElementTree.SubElement(root, 'Name')
        element.text = procedure_name
        element = ElementTree.SubElement(root, 'Para')
        element.text = para
        data = ElementTree.tostring(root)
        return data

    @staticmethod
    def decap_input(data):
        """ Parse xml string into structured data when agent receives request.
        """
        procedure_name = None
        para = None
        id = None
        root = ElementTree.fromstring(data)
        if root.tag == 'Procedure':
            for element in root:
                if element.tag == 'UUID':
                    id = uuid.UUID(element.text)
                elif element.tag == 'Name':
                    procedure_name = element.text
                elif element.tag == 'Para':
                    para = element.text
        return procedure_name, para, id

    @staticmethod
    def encap_output(result, id):
        """ Encapsulate data into xml string when agent sends response back.
        """
        root = ElementTree.Element('Feedback')
        element = ElementTree.SubElement(root, 'UUID')
        element.text = str(id)
        element = ElementTree.SubElement(root, 'Result')
        element.text = result
        data = ElementTree.tostring(root)
        return data

    @staticmethod
    def decap_output(data):
        """ Parse xml string into structured data when master receives response.
        """
        feedback = None
        id = None
        root = ElementTree.fromstring(data)
        if root.tag == 'Feedback':
            for element in root:
                if element.tag == 'UUID':
                    id = uuid.UUID(element.text)
                elif element.tag == 'Result':
                    feedback = element.text
        return feedback, id

    @staticmethod
    def check_termination(message_queue, request_dict):
        """ Judge whether all requests have been answered by agent. message_queue is a dict stores all responses from
            agent while request_dict is a dict stores all requests from master.
        """
        # traverse message_queue
        for key in message_queue:
            while not message_queue[key].empty():
                result = message_queue[key].get()
                feedback, id = DcaProtocol.decap_output(result)     # extract data from message_queue
                request_dict[id] = feedback     # according to uuid, get the corresponding feedback

        # judge if all requests have been answered
        request_clear = True
        for key in request_dict:
            if not request_dict[key]:
                request_clear = False

        return request_clear
