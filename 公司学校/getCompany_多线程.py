import requests
from bs4 import BeautifulSoup
import threading
import time


class CrawlerThread(threading.Thread):
    """多线程访问网址"""

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        fail = True
        while fail:
            try:
                # print('正在访问%s' % self.url)
                r = requests.get(self.url, timeout=5)  # 访问每个子分类中第一页信息
                page = r.text
                self.getMessage(page)
                pageUrls = self.createUrls(self.url, page)
                for url in pageUrls:  # 每个页面有多少页对应多少url
                    tag = True
                    while tag:
                        try:
                            r = requests.get(url, timeout=5)
                            page = r.text
                            self.getMessage(page)
                            tag = False
                        except Exception as e:
                            print('访问%s无效' % url)
                fail = False
            except Exception as e:
                print('访问%s失败' % self.url, e)

    def createUrls(self, url, page):
        '''获取分类中有多少页, 记录每页的地址'''
        soup = BeautifulSoup(page, 'lxml')
        pageNum = int(soup.find('font').string)
        pageUrl = []
        n = url.rfind('p') + 1  # 右边最后一个p的index
        for i in range(2, pageNum + 1):
            url = url[:n] + repr(i) + '.html'
            pageUrl.append(url)
        return pageUrl

    def getMessage(self, page):
        '''获取页面所需要公司信息'''
        soup = BeautifulSoup(page, 'lxml')
        tds = soup.find_all('td', class_='tItem')
        companies = []
        for td in tds:
            companyName = td.find('a').string
            if companyName is not None:
                company = td.find('a').string + '\n'
                companies.append(company)
        self.saveMessage(companies)

    def saveMessage(self, textList):
        with open('companies_c.txt', 'a', encoding='utf-8') as f:
            f.writelines(textList)


class Crawler(object):
    """爬取公司名字的爬虫"""

    def __init__(self, urls, threadnum):
        super(Crawler, self).__init__()
        self.threadnum = threadnum
        self.urls = urls

    def craw(self):
        threads = []
        for i in range(self.threadnum):
            thread = CrawlerThread(self.urls[i])
            threads.append(thread)
        for i in range(self.threadnum):
            threads[i].start()
        for i in range(self.threadnum):
            threads[i].join()


def getUrl():
    with open('company.txt', 'r', encoding='utf-8') as f:
        urls = []
        for line in f.readlines():
            line = line.strip('\n')
            urls.append(line)
    return urls


def main():
    threadNum = 200  # 线程数
    urls = getUrl()
    for i in range(int(len(urls) / threadNum)):
        newUrls = urls[0:threadNum]  # 取urls前与线程数相等的小列表
        crawler = Crawler(newUrls, threadNum)
        crawler.craw()
        print('已获取到网址%s' % newUrls[-1])
        del urls[0:threadNum]
    if urls != []:
        crawler = Crawler(urls, len(urls))
        crawler.craw()


if __name__ == '__main__':
    main()
