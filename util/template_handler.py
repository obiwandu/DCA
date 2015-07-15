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

        str_xml = ElementTree.tostring(root) + '\n'
        fp = open(self.template_path, 'a+')
        for line in fp:
            if str_xml == line:
                fp.close()
                return

        fp.write(str_xml)
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
                        if sub_element.tag == 'AbsCmd':
                            cmd.abs_cmd = sub_element.text
                        elif sub_element.tag == 'ActCmd':
                            cmd.act_cmd = sub_element.text
                        elif sub_element.tag == 'ExpResult':
                            for field in sub_element:
                                cmd.exp_result.append((field.tag, field.text))
                        else:
                            setattr(cmd, sub_element.tag, sub_element.text)
                if element.tag == 'DevInfo':
                    for sub_element in element:
                        if sub_element.tag == 'Type':
                            dev_info.dev_type = sub_element.text
                        elif sub_element.tag == 'Factory':
                            dev_info.dev_factory = sub_element.text
                        elif sub_element.tag == 'Model':
                            dev_info.dev_model = sub_element.text
                        else:
                            setattr(cmd, sub_element.tag, sub_element.text)
        return cmd, dev_info

    def config_path(self, new_path):
        self.template_path = new_path
