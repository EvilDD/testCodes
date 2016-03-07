# -*- coding:utf-8 -*-
from urllib import parse, request
from urllib.error import URLError
import threading


class api_request():

    def __init__(self, url, data, interface_name):
        self.url = url
        self.data = data
        self.interface_name = interface_name

    def post(self):
        data = self.data
        data = parse.urlencode(data).encode('utf-8')
        try:
            req = request.Request(self.url, data)
            rep = request.urlopen(req)
            reps = rep.read().decode('utf-8')
            print('interface_name:\n', self.interface_name)
            print('responsed_code:\n', reps)
        except URLError as e:
            print(e)


def api_method():

    url = 'http://dev.ihaixie.com/shop/index.php?act=member_order&op=payOrder'
    data = {'u': 'zyd', 'p': '339c3e65a545716b202144dc5e13601c',
            'pay_sn': '300504014252437006'}
    interface = 'paySn_interface'
    method = api_request(url, data, interface)
    return method.post()

try:
    i = 0
    tasks = []
    task_number = 1
    while i < task_number:
        t = threading.Thread(target=api_method())
        tasks.append(t)
        t.start()
        i += 1
except Exception as e:
    print(e)
