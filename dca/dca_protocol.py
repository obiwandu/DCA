from xml.etree import ElementTree
__author__ = 'User'

class DcaProtocol:
    def __init__(self):
        pass

    @staticmethod
    def encap(procedure_name, para):
        root = ElementTree.Element('Procedure')
        element = ElementTree.SubElement(root, 'Name')
        element.text = procedure_name
        element = ElementTree.SubElement(root, 'Para')
        element.text = para
        data = ElementTree.tostring(root)
        return data

    @staticmethod
    def decap(data):
        root = ElementTree.fromstring(data)
        if root.tag == 'Procedure':
            for element in root:
                if element.tag == 'Name':
                    procedure_name = element.text
                if element.tag == 'Para':
                    para = element.text
        return procedure_name, para