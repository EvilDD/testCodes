import json
import threading
from urllib.request import urlopen
import time
path = 'D:/我的文档/桌面/1.txt'


class getIdcarThread(threading.Thread):

    """多线程获取idCard"""

    def __init__(self, url):
        # super(getIdcarThread, self).__init__()
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        self.getIdcard(self.url)

    def getIdcard(self, url):
        try:
            rep = urlopen(url).read().decode('utf-8')
            dic = json.loads(rep)
            if 'identityCardNum' in dic["jingdong_pop_customs_getIdentityCardNoByOrderId_responce"]["getIdentityCardNoByOrderId_result"]:
                print(dic["jingdong_pop_customs_getIdentityCardNoByOrderId_responce"][
                      "getIdentityCardNoByOrderId_result"]["identityCardNum"])
            else:
                print('身份证获取失败！')
        except:
            print('网络无法联接！')


def getUrls(path):
    url = 'https://api.jd.com/routerjson?v=2.0&method=jingdong.pop.customs.getIdentityCardNoByOrderId'
    app_key = 'C95725512D071B077BB3CA72E6B6CC5'  # app_key:6
    access_token = 'dfd67b13-50e6-4a03-a074-c2db7ddd6e7d'
    urls = []
    try:
        orders = open(path, 'r', encoding='utf-8')
        orderIds = orders.readlines()
        orders.close()
    except Exception:
        orderIds = []
        print("没有找到该文件！")
    # if orderIds != []:
    for orderId in orderIds:
        orderId = orderId.strip('\ufeff\n ')
        param_json = '{"vId":"182434","orderId":"' + orderId + '"}'
        temp_url = url + '&app_key=' + app_key + '&access_token=' + \
            access_token + '&360buy_param_json=' + param_json
        urls.append(temp_url)
    return urls


def main():
    threads = []
    urls = getUrls(path)
    urlCount = len(urls)
    st = time.time()
    for x in range(urlCount):
        t = getIdcarThread(urls[x])
        threads.append(t)
    for y in range(urlCount):
        threads[y].start()
    for z in range(urlCount):
        threads[z].join()
    et = time.time()
    print('消费时间:%f' % (et - st))
if __name__ == '__main__':
    main()
