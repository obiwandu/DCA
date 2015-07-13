from xml.etree import ElementTree

from util.datastructure import Command, DevInfo


class TemplateHandler:
    def __init__(self):
        self.template_path = 'template\\template.xml'
        return

    def to_template(self, command, dev_info):
        root = ElementTree.Element('Template')

        cmd = ElementTree.SubElement(root, 'Command')
        element = ElementTree.SubElement(cmd, 'AbsCmd')
        element.text = command.abs_cmd
        element = ElementTree.SubElement(cmd, 'ActCmd')
        element.text = command.act_cmd
        element = ElementTree.SubElement(cmd, 'ExpResult')
        for field in command.exp_result:
            res = ElementTree.SubElement(element, '%s' % field[0])
            res.text = field[1]

        dev = ElementTree.SubElement(root, 'DevInfo')
        element = ElementTree.SubElement(dev, 'Type')
        element.text = dev_info.dev_type
        element = ElementTree.SubElement(dev, 'Factory')
        element.text = dev_info.dev_factory
        element = ElementTree.SubElement(dev, 'Model')
        element.text = dev_info.dev_model

        str_xml = ElementTree.tostring(root)
        fp = open(self.template_path, 'a')
        fp.write(str_xml + "\n")
        fp.close()
        return

    @staticmethod
    def parse_template(str_xml):
        dev_info = DevInfo()
        cmd = Command()

        root = ElementTree.fromstring(str_xml)
        if root.tag == 'Template':
            for element in root:
                if element.tag == 'Command':
                    for sub_element in element:
                        if sub_element.tag != 'ExpResult':
                            setattr(cmd, sub_element.tag, sub_element.text)
                        else:
                            for field in sub_element:
                                cmd.exp_result.append((field.tag, field.text))
                if element.tag == 'DevInfo':
                    for subElement in element:
                        setattr(dev_info, subElement.tag, subElement.text)
        return cmd, dev_info

    def config_path(self, new_path):
        self.template_path = new_path
