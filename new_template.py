__author__ = 'User'
"""it's a data structure that stores all template data, and can be converted into xml conveniently"""
import xml.etree.ElementTree as ET

class TemplateNew:
    def __init__(self):
        self.cmd = dict()
        self.exp_res = []
        self.exec_para = dict()
        self.executable = False
        self.accessible = False
        return

    def init(self, abs_cmd, act_cmd, factory, model, exp_res):
        self.cmd['abs_cmd'] = abs_cmd
        self.cmd['act_cmd'] = act_cmd
        self.cmd['factory'] = factory
        self.cmd['model'] = model
        self.exp_res = exp_res
        # self.exec_para['ip'] = ''
        # self.exec_para['dev_id'] = ''
        # self.exec_para['dev_pw'] = ''
        self.accessible = True
        self.executable = False
        return

    def from_xml(self, str_xml):
        self.parse_xml(str_xml)
        self.accessible = True
        self.executable = True
        return

    # def __init__(self, str_xml, abs_cmd='', act_cmd='', factory='', model='', exp_res=[]):
    #     self.cmd = dict()
    #     self.exp_res = []
    #     self.exec_para = dict()
    #     if not str_xml:
    #         self.cmd['abs_cmd'] = abs_cmd
    #         self.cmd['act_cmd'] = act_cmd
    #         self.cmd['factory'] = factory
    #         self.cmd['model'] = model
    #         self.exp_res = exp_res
    #         # self.exec_para['ip'] = ''
    #         # self.exec_para['dev_id'] = ''
    #         # self.exec_para['dev_pw'] = ''
    #         self.executable = False
    #     else:
    #         self.parse_xml(str_xml)
    #         self.executable = True
    #     return

    def parse_xml(self, str_xml):
        root = ET.fromstring(str_xml)
        for element in root:
            if element.tag == 'cmd':
                for subElement in element:
                    self.cmd['%s' % subElement.tag] = subElement.text
            elif element.tag == 'exp_res':
                for subElement in element:
                    self.exp_res.append((subElement.tag, subElement.text))
            elif element.tag == 'exec_para':
                for subElement in element:
                    self.exec_para['%s' % subElement.tag] = subElement.text
        # return template, expect_result
        return

    def to_xml(self):
        if self.accessible:
            root = ET.Element('template')
            cmd = ET.SubElement(root, 'cmd')
            for key in self.cmd.keys():
                element = ET.SubElement(cmd, '%s' % key)
                element.text = self.cmd['%s' % key]
            exp_res = ET.SubElement(root, 'exp_res')
            for field in self.exp_res:
                element = ET.SubElement(exp_res, '%s' % field[0])
                element.text = field[1]
            if self.executable:
                exec_para = ET.SubElement(root, 'exec_para')
                for key in self.exec_para.keys():
                    element = ET.SubElement(exec_para, '%s' % key)
                    element.text = self.exec_para['%s' % key]
            # ET.dump(root)
            return ET.tostring(root)
        return

    def append(self, ip, dev_id, dev_pw):
        if self.accessible:
            self.exec_para['ip'] = ip
            self.exec_para['dev_id'] = dev_id
            self.exec_para['dev_pw'] = dev_pw
            self.executable = True
        return

    def find(self):
        return

"""simplest template creation, not executable"""
def tc1():
    print "---------------tc 1 start-----------------"
    exp_res = [("output1", "\w"), ("output2", "\d")]
    tmp = TemplateNew()
    tmp.init("ipconfig", "ifconfig -hw", "hw", "150", exp_res)
    print tmp.cmd
    print tmp.exp_res
    print tmp.exec_para
    print "---------------tc 1 end-----------------"
    return

"""simplest template creation, not executable, convert to xml"""
def tc2():
    print "---------------tc 2 start-----------------"
    exp_res = [("output1", "\w"), ("output2", "\d")]
    tmp = TemplateNew()
    tmp.init("ipconfig", "ifconfig -hw", "hw", "150", exp_res)
    print tmp.to_xml()
    print "---------------tc 2 end-----------------"

"""simplest template creation, not executable, convert from xml"""
def tc3():
    print "---------------tc 3 start-----------------"
    str_xml = "<template><cmd><model>150</model><act_cmd>ifconfig -hw</act_cmd><factory>hw</factory><abs_cmd>ipconfig</abs_cmd></cmd><exp_res><output1>\w</output1><output2>\d</output2></exp_res></template>"
    tmp = TemplateNew()
    tmp.from_xml(str_xml)
    print tmp.cmd
    print tmp.exp_res
    print tmp.exec_para
    print "---------------tc 3 end-----------------"

"""executable template creation, convert to xml"""
def tc4():
    print "---------------tc 4 start-----------------"
    exp_res = [("output1", "\w"), ("output2", "\d")]
    tmp = TemplateNew()
    tmp.init("ipconfig", "ifconfig -hw", "hw", "150", exp_res)
    tmp.append("1.1.1.1", "root", "123456")
    print tmp.to_xml()
    print "---------------tc 4 end-----------------"

"""executable template creation, convert from xml"""
def tc5():
    print "---------------tc 5 start-----------------"
    str_xml = "<template><cmd><model>150</model><act_cmd>ifconfig -hw</act_cmd><factory>hw</factory><abs_cmd>ipconfig</abs_cmd></cmd><exp_res><output1>\w</output1><output2>\d</output2></exp_res><exec_para><dev_pw>123456</dev_pw><ip>1.1.1.1</ip><dev_id>root</dev_id></exec_para></template>"
    tmp = TemplateNew()
    tmp.from_xml(str_xml)
    print tmp.cmd
    print tmp.exp_res
    print tmp.exec_para
    print "---------------tc 5 end-----------------"

if __name__ == "__main__":
    tc1()
    tc2()
    tc3()
    tc4()
    tc5()