import xml.etree.ElementTree as ET
import json

class Template:
    def __init__(self):
        self.tempDict = dict()
        self.count = 0
        return

    @staticmethod
    def parse_temp(temp_str):
        template = dict()
        expect_result = []
        root = ET.fromstring(temp_str)
        for element in root:
            if element.tag != 'expect_result':
                template['%s' % element.tag] = element.text
            else:
                for subElement in element:
                    expect_result.append(subElement.tag, subElement.text)

        return template, expect_result

    def create_temp(self, abs_cmd, ip, factory, act_cmd):
        new_template = dict()
        new_template['abs_cmd'] = abs_cmd
        new_template['ip'] = ip
        new_template['factory'] = factory
        new_template['act_cmd'] = act_cmd
        new_template['xmlStr'] = self.generate_xml(new_template)
        new_template_str = new_template['xmlStr']
        self.count += 1
        # self.tempDict['%s' % self.count] = new_template_str
        self.tempDict[(abs_cmd, ip, factory)] = new_template_str
        return self.count, new_template_str

    def create_temp_disk(self, abs_cmd, factory, act_cmd, expect_result):
        new_template = dict()
        new_template['abs_cmd'] = abs_cmd
        new_template['factory'] = factory
        new_template['act_cmd'] = act_cmd
        new_template_str = self.generate_xml(new_template, expect_result)
        self.count += 1
        file = open('template', 'a')
        # json.dump(new_template_str, file)
        file.write(new_template_str + "\n")
        file.close()
        return new_template_str

    @staticmethod
    def generate_xml(template, expect_result):
        root = ET.Element('root')
        for key in template.keys():
            element = ET.SubElement(root, '%s' % key)
            element.text = template['%s' % key]
        result = ET.SubElement(root, 'expect_result')
        for field in expect_result:
            element = ET.SubElement(result, '%s' % field[0])
            element.text = field[1]
        # ET.dump(root)
        return ET.tostring(root)

    @staticmethod
    def parse_xml(template_str):
        template = dict()
        expcet_result = []
        root = ET.fromstring(template_str)
        for element in root:
            template['%s' % element.tag] = element.text
            #parse result
        return template, expcet_result

    def find_temp(self, abs_cmd, ip, factory):
        if (abs_cmd, ip, factory) in self.tempDict:
            return self.tempDict[(abs_cmd, ip, factory)]
        else:
            return

    def find_temp_disk(self, abs_cmd, factory):
        filedes = open('template', 'r')
        # temp_dict = json.load(file)
        for line in filedes:
            print "print line:", line
            template, expect_result = self.parse_temp(line)
            print "template:", template
            if template['abs_cmd'] == abs_cmd and template['factory'] == factory:
                return template
        return

def testcase_cfg_and_genXML():
    tmp = Template()
    res = tmp.create_temp("show cfg", "1.1.1.1", "H3C", "show cfg on H3C")
    # print "create template"
    # print res
    parse_res = Template.parse_temp(res[1])
    # print "parse template"
    # print parse_res

if __name__ == "__main__":
    # testcase_gen_xml()
    testcase_cfg_and_genXML()
