# -*- coding:utf-8 -*-
import threading
import queue
import requests
from bs4 import BeautifulSoup
import re

exitFlag = 0  # 通知线程啥时候退出
queueLock = threading.Lock()


class CrawlerThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q  # 队列

    def run(self):
        global exitFlag
        while not exitFlag:
            queueLock.acquire()
            if not self.q.empty():
                self.url = self.q.get()
                print(self.url, self.q.qsize())
                queueLock.release()
                tag = True
                while tag:
                    try:
                        r = requests.get(self.url, timeout=5)
                        tag = False
                        r.encoding = 'gbk'
                        pageSouce = r.text
                        soup = BeautifulSoup(pageSouce, 'lxml')
                        self.getSchool(soup)
                        if self.url[-1:] is '/':  # 以/结尾则在抓取第1页
                            pagesUrl = self.creatUrl(soup)
                            if pagesUrl is not None:  # 判断是否只有一页,不止就加队列
                                queueLock.acquire()
                                for pageUrl in pagesUrl:
                                    self.q.put(pageUrl)
                                queueLock.release()
                    except Exception as e:
                        print('获取%s失败\n原因%s' % (self.url, e))
            else:
                queueLock.release()

    def getSchool(self, soup):
        '''抓取学校名字并保存'''
        schools = soup.find(class_='list-xx').find_all('p')
        schoolsName = []
        for s in schools:
            schoolName = s.string + '\n'
            schoolsName.append(schoolName)
        self.saveSchool(schoolsName)

    def creatUrl(self, soup):
        '''创建第2页到时最后一页url,列表返回,如果只有一页返回None'''
        '''/youeryuan/pn8.html'''
        lastEle = soup.find(class_='last')
        if lastEle is not None:
            lastUrl = lastEle.get('href')
            pageNum = re.search('\d+', lastUrl).group()
            pagesUrl = []
            for i in range(int(pageNum)):
                tmpUrl = self.url + 'pn' + repr(i + 2) + '.html'  # 第二页至最后一页
                pagesUrl.append(tmpUrl)
            return pagesUrl
        else:
            return None

    def saveSchool(self, textList):
        with open('学校.txt', 'a', encoding='utf-8') as f:
            f.writelines(textList)


def main():
    url = 'http://www.xuexiaodaquan.com'
    try:
        r = requests.get(url, timeout=5)
        pageSouce = r.text
        urls = getAreasUrl(pageSouce)
    except Exception as e:
        print('%s访问失败\n原因:%s' % (url, e))
    workQueue = queue.Queue()
    threadNum = 300  # 线程数
    threads = []  # 线程池
    queueLock.acquire()
    for url in urls:
        workQueue.put(url)  # 填充队列
    queueLock.release()
    for i in range(threadNum):
        thread = CrawlerThread(workQueue)
        thread.start()
        threads.append(thread)
    while not workQueue.empty():  # 等待队列清空
        pass
    global exitFlag
    exitFlag = 1
    for t in threads:
        t.join()


def getAreasUrl(pageSouce):
    soup = BeautifulSoup(pageSouce, 'lxml')
    areas = soup.find(class_='city-all').find_all('a')
    urls = []
    for area in areas:
        url = area.get('href')
        if url != '#':
            tmpUrl = url + 'youeryuan/'  # 幼儿园
            urls.append(tmpUrl)
            tmpUrl = url + 'xiaoxue/'  # 小学
            urls.append(tmpUrl)
            tmpUrl = url + 'chuzhong/'  # 初中
            urls.append(tmpUrl)
            tmpUrl = url + 'gaozhong/'  # 高中
            urls.append(tmpUrl)
            tmpUrl = url + 'daxue/'  # 大学
            urls.append(tmpUrl)
            tmpUrl = url + 'chengrenjiaoyu/'  # 成人教育
            urls.append(tmpUrl)
            tmpUrl = url + 'peixunjigou/'  # 培训机构
            urls.append(tmpUrl)
    return urls


if __name__ == '__main__':
    main()
