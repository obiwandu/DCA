from util.datastructure import DevInfo

class DeviceManagemnt:
    def __init__(self):
        return

    @staticmethod
    def get_devinfo(ip):
        devinfo = DevInfo()
        if ip == '1.1.1.1':
            devinfo.dev_type = 'switch'
            devinfo.dev_factory = 'HW'
            devinfo.dev_model = '150'
            agent_ip = '127.0.0.1'
        elif ip == '192.168.0.1':
            devinfo.dev_type = 'switch'
            devinfo.dev_factory = 'CISCO'
            devinfo.dev_model = '200'
            agent_ip = '127.0.0.1'
        elif ip == '10.65.7.131':  #taobao test device
            devinfo.dev_type = 'server'
            devinfo.dev_factory = 'ALIBABA'
            devinfo.dev_model = 'taobao_test'
            agent_ip = '127.0.0.1'
        elif ip == '10.137.59.22':  # springboard
            devinfo.dev_type = 'server'
            devinfo.dev_factory = 'ALIBABA'
            devinfo.dev_model = 'springboard'
            agent_ip = '127.0.0.1'
        else:
            devinfo.dev_type = 'switch'
            devinfo.dev_factory = 'HW'
            devinfo.dev_model = '150'
            agent_ip = '127.0.0.1'
        return agent_ip, devinfo
