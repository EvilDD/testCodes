import requests
from bs4 import BeautifulSoup
import queue
import threading
import time

with open('company.txt', 'r', encoding='utf-8') as f:
    urls = []
    for line in f.readlines():
        line = line.strip('\n')
        urls.append(line)


def visitUrl(url):
    fail = True
    while fail:
        try:
            r = requests.get(url, timeout=5)
            page = r.text
            fail = False
        except Exception as e:
            print('访问%s失败' % url, e)
    return page


def createUrls(url, page):
    '''获取分类中有多少页,记录每页的地址'''
    soup = BeautifulSoup(page, 'lxml')
    pageNum = int(soup.find('font').string)
    pageUrl = []
    n = url.rfind('p') + 1  # 右边最后一个p的index
    for i in range(2, pageNum + 1):
        url = url[:n] + repr(i) + '.html'
        pageUrl.append(url)
    return pageUrl


def getMessage(page):
    '''获取页面所需要公司信息'''
    soup = BeautifulSoup(page, 'lxml')
    tds = soup.find_all('td', class_='tItem')
    companies = []
    for td in tds:
        companyName=td.find('a').string
        if companyName is not None:
            company = td.find('a').string + '\n'
            companies.append(company)
    return companies


def saveMessage(textList):
    with open('companies_b.txt', 'a', encoding='utf-8') as f:
        f.writelines(textList)


def main():
    for url in urls:
        page = visitUrl(url)  # 获取第一页
        pageUrls = createUrls(url, page)  # 此分类一共有多少页
        companies = getMessage(page)  # 获取第一页公司信息
        saveMessage(companies)
        print('保存成功' + url)
        if pageUrls != []:  # 有些小分类只有一页
            for pageUrl in pageUrls:
                page = visitUrl(pageUrl)
                companies = getMessage(page)  # 如有多页循环获取第二页以后的公司信息
                saveMessage(companies)
                print('保存成功' + pageUrl)


if __name__ == '__main__':
    main()
