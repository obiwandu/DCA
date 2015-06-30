import xml.etree.ElementTree as ET
from datastructure import Command
from datastructure import Identity

class Template:
    def __init__(self):
        self.template_path = 'template.xml'
        return

    def to_template(self, command, identity):
        cmd = Command()
        ident = Identity()

        cmd.abs_cmd = command.abs_cmd
        cmd.act_cmd = command.act_cmd
        cmd.exp_result = command.exp_result
        ident.dev_type = identity.dev_type
        ident.dev_factory = identity.dev_factory
        ident.dev_model = identity.dev_model
        str_xml = Template.to_xml(cmd, ident)
        self.save(str_xml)
        return

    @staticmethod
    def to_xml(command, identity):
        root = ET.Element('template')

        cmd = ET.SubElement(root, 'command')
        element = ET.SubElement(cmd, 'abs_cmd')
        element.text = command.abs_cmd
        element = ET.SubElement(cmd, 'act_cmd')
        element.text = command.act_cmd
        exp_res = ET.SubElement(cmd, 'exp_result')
        for field in command.exp_result:
            element = ET.SubElement(exp_res, '%s' % field[0])
            element.text = field[1]

        ident = ET.SubElement(root, 'identity')
        if identity.ip:
            element = ET.SubElement(ident, 'ip')
            element.text = identity.ip
        if identity.dev_id:
            element = ET.SubElement(ident, 'dev_id')
            element.text = identity.dev_id
        if identity.dev_pw:
            element = ET.SubElement(ident, 'dev_pw')
            element.text = identity.dev_pw
        element = ET.SubElement(ident, 'dev_type')
        element.text = identity.dev_type
        element = ET.SubElement(ident, 'dev_factory')
        element.text = identity.dev_factory
        element = ET.SubElement(ident, 'dev_model')
        element.text = identity.dev_model

        return ET.tostring(root)

    @staticmethod
    def parse_xml(str_xml):
        command = Command()
        identity = Identity()
        root = ET.fromstring(str_xml)
        for element in root:
            if element.tag == 'command':
                for subElement in element:
                    if subElement.tag != 'exp_result':
                        setattr(command, subElement.tag, subElement.text)
                    else:
                        for field in subElement:
                            command.exp_result.append((field.tag, field.text))
            elif element.tag == 'identity':
                for subElement in element:
                    setattr(identity, subElement.tag, subElement.text)
        return command, identity

    def config_path(self, new_path):
        self.template_path = new_path

    def find(self, abs_cmd, ident):
        try:
            fp = open(self.template_path, 'r')
        except IOError, e:
            print 'Template file %s not found.' % e
            return

        command = Command()
        identity = Identity()
        for line in fp:
            # print "print line:", line
            command, identity = Template.parse_xml(line)
            if command.abs_cmd == abs_cmd and identity.dev_type == ident.dev_type and identity.dev_factory == ident.dev_factory and identity.dev_model == ident.dev_model:
                return line
            # cmd, exp_res, exec_para = TemplateNew.parse_xml(line)
            # print cmd
            # print exp_res
            # print exec_para
            # if cmd['abs_cmd'] == abs_cmd and cmd['factory'] == factory and cmd['model'] == model:
            #     return line
        return

    def save(self, str_xml):
        fp = open(self.template_path, 'a')
        fp.write(str_xml + "\n")
        fp.close()
        return

