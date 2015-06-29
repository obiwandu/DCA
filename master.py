#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by lingjiao.lc

"""
Note, in my script, a tab equals four blanks.
You must have a check of your indentation.
"""

import os
import sys
import md5
import json
from eos.lib.http import HTTP
from template import Template
import getpass
from device_mngt import DeviceManagemnt
import httplib, urllib
from new_template import TemplateNew
from datastructure import Identity, Command
from cmdline_interface import CmdLineInterface

class Master:
    def __init__(self, inputIf):
        # init the input interface
        self.inputIf = inputIf()
        self.ip = None
        self.dev_id = None
        self.dev_pw = None
        self.factory = None
        self.model = None
        self.logged = False

        self.identity = Identity()
        self.command = Command()
        return

    def test(self):
        ip =  "10.65.254.70"
        userid = ""
        pw = "huawei123"

        dev = DeviceManagemnt()
        factory, model = dev.get_factory(ip)
        abs_cmd = "dir"

        str_xml = TemplateNew.find(abs_cmd, factory, model)
        temp = TemplateNew()
        # template = self.temp.find_temp_disk(abs_cmd, factory)
        if str_xml:
            temp.from_xml(str_xml)
            temp.append(ip, userid, pw)
            http_request(temp.to_xml())
        # else:
        #     act_cmd = raw_input("No template found. Input the actual command:")
        #     temp.from_para(abs_cmd, act_cmd, factory, model, exp_res)
        #     template_str = self.temp.create_temp_disk(abs_cmd, factory, act_cmd)
        #     template = Template.parse_xml(template_str)
        #     template['ip'] = ip
        #     template['userid'] = userid
        #     template['pw'] = pw
        #     template_str = Template.generate_xml(template)
        #     http_request(template_str)
        return

    def login(self):
        self.inputIf.login(self.identity)
        dev = DeviceManagemnt()
        self.identity.factory, self.identity.model = dev.get_factory(self.identity.ip)
        self.logged = True
        return

    def cfg_cmd(self):
        if self.logged:
            self.inputIf.cfg_cmd(self.command)
            temp = TemplateNew()
            temp.from_para(self.command.abs_cmd, self.command.act_cmd, self.identity.factory, self.identity.model, self.command.exp_res)
            temp.save()
        return

    def exec_cmd(self):
        if self.logged:
            self.inputIf.exec_cmd(self.command)
            temp = TemplateNew()
            # str_xml = TemplateNew.find(self.command.abs_cmd, self.identity.factory, self.identity.model)
            str_xml = temp.find(self.command.abs_cmd, self.identity.factory, self.identity.model)
            if str_xml:
                # temp = TemplateNew()
                temp.from_xml(str_xml)
                temp.append(self.identity.ip, self.identity.dev_id, self.identity.dev_pw)
                final_str_xml = temp.to_xml()
                return http_request(final_str_xml)
        return

    def show_temp(self):
        # print self.temp.tempDict
        return

    # def cfg_cmd(self):
    #     abs_cmd = raw_input("Input the abstract command:")
    #     act_cmd = raw_input("Input the actual command:")
    #     factory = raw_input("Input the factory:")
    #     ip = raw_input("Input the IP address:")
    #     self.temp.create_temp(abs_cmd, ip, factory, act_cmd)
    #     return

    # def cfg_cmd_main(self):

    def cfg_cmd_disk(self):
        temp = TemplateNew()

        abs_cmd = raw_input("Input the abstract command:")
        factory = raw_input("Input the factory:")
        model = raw_input("Input the model:")
        act_cmd = raw_input("Input the actual command:")
        result_cnt = raw_input("Input the number of result field:")
        expect_result = []
        for i in range(int(result_cnt)):
            key = raw_input("Input the key of result:")
            val = raw_input("Input the regular expression of result:")
            expect_result.append((key, val))

        temp.from_para(abs_cmd, act_cmd, factory, model, expect_result)
        temp.save()
        # self.temp.create_temp_disk(abs_cmd, factory, act_cmd, expect_result)
        return

    # def exec_cmd(self):
    #     abs_cmd = raw_input("Input the abstract command:")
    #     factory = raw_input("Input the factory:")
    #     ip = raw_input("Input the IP address:")
    #
    #     temp_str = self.temp.find_temp(abs_cmd, ip, factory)
    #     if temp_str:
    #         print "Template:", temp_str
    #         http_request(temp_str)
    #     else:
    #         act_cmd = raw_input("No template found. Input the actual command:")
    #         count, template_str = self.temp.create_temp(abs_cmd,ip,factory,act_cmd)
    #         http_request(template_str)
    #
    #     # http_request(abs_cmd, ip, factory)
    #     return

    def exec_script(self):
        ip = raw_input("Input the IP address:")
        dev_id = raw_input("Input the device user id:")
        dev_pw = getpass.getpass()

        dev = DeviceManagemnt()
        factory, model = dev.get_factory(ip)

        script_name = raw_input("Input the script to be executed:")
        return

    def exec_cmd_disk(self):
        temp = TemplateNew()

        ip = raw_input("Input the IP address:")
        dev_id = raw_input("Input the device user id:")
        dev_pw = getpass.getpass()

        dev = DeviceManagemnt()
        factory, model = dev.get_factory(ip)

        abs_cmd = raw_input("Input the abstract command:")

        str_xml = TemplateNew.find(abs_cmd, factory, model)
        # template, expect_result = self.temp.find_temp_disk(abs_cmd, factory)
        if str_xml:
            # print "matched XML:", str_xml
            temp.from_xml(str_xml)
            temp.append(ip, dev_id, dev_pw)
            final_str_xml = temp.to_xml()
            # print "final XML:", final_str_xml
            http_request(final_str_xml)
        else:
            act_cmd = raw_input("No template found. Input the actual command:")
            result_cnt = raw_input("Input the number of result field:")
            expect_result = []
            for i in range(int(result_cnt)):
                key = raw_input("Input the key of result:")
                val = raw_input("Input the regular expression of result:")
                expect_result.append((key, val))
            temp.from_para(abs_cmd, act_cmd, factory, model, expect_result)
            temp.save()
            temp.append(ip, dev_id, dev_pw)
            final_str_xml = temp.to_xml()
            # print "final XML:", final_str_xml
            http_request(final_str_xml)

        # http_request(abs_cmd, ip, factory)
        return

def http_request(template_str):
    http_client = None
    ret = ""
    try:
        uri = template_str
        # ret = HTTP("0.0.0.0", 8000).get(uri)
        ret = HTTP("127.0.0.1", 8000).get(uri)

        print "**************************"
        print "start printing response:"
        print ret
        print "**************************"

    except Exception, e:
        print "Print exception:"
        print e
    finally:
        if http_client:
            http_client.close()
    return ret

def start_master1():
    master = Master(CmdLineInterface)
    while True:
        opr_type = raw_input("operation type:")
        # if opr_type == "cfg":
        #     master.cfg_cmd()
        # elif opr_type == "exec":
        #     master.exec_cmd()
        if opr_type == "show temp":
            master.show_temp()
        elif opr_type == "cfg":
            master.cfg_cmd_disk()
        elif opr_type == "exec":
            master.exec_cmd_disk()
        elif opr_type == "test":
            master.test()
        elif opr_type == "script":
            master.exec_script()

def start_master2():
    master = Master(CmdLineInterface)
    master.login()
    while True:
        opr_type = raw_input("operation type:")
        # if opr_type == "cfg":
        #     master.cfg_cmd()
        # elif opr_type == "exec":
        #     master.exec_cmd()
        if opr_type == "show temp":
            master.show_temp()
        elif opr_type == "cfg":
            master.cfg_cmd()
        elif opr_type == "exec":
            master.exec_cmd()
        elif opr_type == "test":
            master.test()
        elif opr_type == "script":
            master.exec_script()

if __name__ == "__main__":
    start_master2()
    # Master.exec_cmd("show cfg", "1.1.1.1", "H3C")

