import http.client
import threading
import time

host = 'dev.ihaixie.com'
port = 80
uri = '/shop/index.php?act=goods&op=getstock&u=zyd&p=339c3e65a545716b202144dc5e13601c&s=3963045NA-B'
total = 0  # 总访问数
succ = 0  # 访问成功
fail = 0  # 访问失败
exce = 0  # 异常数
maxtime = 0  # 访问响应时间最大为几秒
mintime = 100  # 访问响应时间最小为几秒
gt = 0  # 访问响应时间高于3秒
lt = 0  # 访问响应时间小于3秒


class request_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.test_percormace()

    def test_percormace(self):
        global total
        global succ
        global fail
        global exce
        global gt
        global lt

        try:
            st = time.time()
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request('GET', uri)
            res = conn.getresponse()
            # 成功或失败，总数加1
            if res.status == 200:
                total += 1
                succ += 1
            else:
                total += 1
                fail += 1
            js = time.time() - st
            print('%s:%f' % (self.name, js))
            # 调用下面方法判断单次访问最大和最小响应时间
            self.max_min(js)
            # 响应时间大于3秒
            if js > 3:
                gt += 1
            else:
                lt += 1
        except Exception as e:
            print(e)
            total += 1
            exce += 1
        conn.close()

    def max_min(self, s):
        global maxtime
        global mintime
        if s > maxtime:
            maxtime = s
        if s < mintime:
            mintime = s


def main():
    at = time.ctime()
    mt = time.time()
    print('开始运行时间:%s' % at)
    print('========================task start=====================')
    global total
    global exce
    thread_count = 500
    threads = []
    for i in range(thread_count):
        t = request_thread()
        threads.append(t)
    for i in range(thread_count):
        try:
            threads[i].start()
        except Exception as e:
            print(e)
            total += 1
            exce += 1
    for j in range(thread_count):
        try:
            threads[j].join()
        except Exception as e:
            print(e)
    print("total:%d,succ:%d,fail:%d,exce:%d" %
          (total, succ, fail, exce))
    print("gt:%d,lt:%d" % (gt, lt))
    print("mintime:%f,maxtime:%f" % (mintime, maxtime))
    print('========================task   end=====================')
    bt = time.ctime()
    nt = time.time()
    jt = mt - nt
    print('结束运行时间:%s' % bt)
    print('%d并发运行消耗总时间:%f' % (thread_count, jt))
if __name__ == '__main__':
    main()
