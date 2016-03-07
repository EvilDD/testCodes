# -*- coding:utf-8 -*-
from urllib.request import urlopen, Request
import re
import os

ordinal = 738  # 表示从第几个作品开始显示，ordinal+=per_page
per_page = 12  # 经测试发现每页显示值的范围为0-25，可配置
pageNum = 30  # 表示此次加载多少页
dirNum = ordinal  # 用来标识创建作品文件标识


def addUrlList():
    '''批量生成url规则加入到url列表中'''
    urls = []
    global ordinal
    global per_page
    global pageNum
    for i in range(pageNum):
        url = 'https://www.behance.net/search?ordinal=' + \
            repr(ordinal) + '&per_page=' + repr(per_page) + \
            '&field=&content=projects&sort=featured_date&time=all&location_id='
        urls.append(url)
        ordinal += per_page
    print('更改ordinal的值可以控制从指定商品开始访问，此次配置:')
    print('url共%d个,每访问一次获取%d个作品,共准备获取%d个作品' % (pageNum, per_page, ordinal))
    return urls


def handleUrl(url):
    '''带cookie访问才能获取html源码，不然只能获取html的js源码'''
    heads = {
        # 'Host': 'www.behance.net',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cookie': 'AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=793872103%7CMCIDTS%7C16815%7CMCMID\
        %7C02799238676487182609051868023608310525%7CMCAAMLH-1453169569%7C11%7CMCAAMB-1453337999\
        %7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; s_pers=%20gpv%3Dbehance.net%7C1452735366340%3B\
        %20s_nr%3D1452733566345-Repeat%7C1484269566345%3B%20s_vs%3D1%7C1452735366528%3B;\
        aam_uuid=92151740275542120342452021992199902892; \
        __utma=6448045.1251196332.1452564771.1452733200.1452733567.6; \
        __utmz=6448045.1452564771.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); \
        bcp=182366; s_sess=%20s_demandbase_v2.2%3Ddone%3B%20s_dmdbase%3D%255Bn%252Fa%255D%253A%255Bn\
        %252Fa%255D%253A%255Bn%252Fa%255D%253A%255Bn%252Fa%255D%253A%255Bn%252Fa%255D%253A%255Bn%252Fa\
        %255D%253AWireless%253AMobile%2520Network%3B%20s_dmdbase_custom%3D%255Bn%252Fa%255D%253A30%253A\
        %255Bn%252Fa%255D%253ACN%253A%255Bn%252Fa%255D%253A%255Bn%252Fa%255D%253A%255Bn%252Fa%255D%253A\
        %255Bn%252Fa%255D%3B%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dwww.behance.net%25252Fsearch\
        %252C33%252C33%252C771%252C0%252C0%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dwww.behance.net\
        %25252F%252C100%252C37%252C4159%252C1920%252C639%252C1920%252C1080%252C1%252CP%3B; __utmc=6448045; s_cc=true; ilo0=true',
        # 'Connection': 'keep-alive',
        # 'Cache-Control': 'max-age=0',
        # 'Referer': 'https://www.behance.net',
        # 'Accept': '*/*',
        # 'X-BCP': '182366',
        # 'X-NewRelic-ID': 'UQYHUlBTGwsHUVBXBgQ=',
        # 'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        req = Request(url, headers=heads)
        rep = urlopen(req)
        html = rep.read().decode('UTF-8')  # 控制台不支持特殊字符输出，需保存到文件查看
    except BaseException as e:
        html = ''
        print(e)
        print('无法打开给出的url:%s' % url)
    rule = '<div class="js-item.*?<!-- #cover-stat-fields-wrap -->\n</div>'
    preCom = re.compile(rule, re.S)
    itemsHtml = re.findall(preCom, html)
    return itemsHtml


def handleHtml(itemHtml):
    '''获取作品链接'''
    rule1 = '<div class="cover-img">.*?"(.*?)"'
    preCom1 = re.compile(rule1, re.S)
    itemLink = re.findall(preCom1, itemHtml)
    '''获取作品样例图片'''
    rule2 = '<img srcset=.*?\s(.*?)\s2x'
    preCom2 = re.compile(rule2, re.S)
    itemPic = re.findall(preCom2, itemHtml)
    '''获取作者名字'''
    rule3 = 'class="js-mini-profile".*?>(.*?)<'
    preCom3 = re.compile(rule3, re.S)
    itemAuth = re.findall(preCom3, itemHtml)
    return itemLink, itemPic, itemAuth


def saveItem(link, pic, auth):
    global dirNum
    path = 'behance/' + repr(dirNum)
    if not os.path.exists(path):
        os.makedirs(path)
    txtPath = path + '/作品信息.txt'
    picPath = path + '/作品样例.jpg'
    f = open(txtPath, 'w', encoding='utf-8')
    f.write('作品展示链接:%s\n作者:%s' % (link, auth))
    f.close()
    try:
        rep = urlopen(pic)
        p = open(picPath, 'wb')
        p.write(rep.read())
        p.close()
    except BaseException as e:
        print('获取保存图片失败', e)
    print('%s保存完毕' % path)


def main():
    global ordinal
    global per_page
    global pageNum
    global dirNum
    urls = addUrlList()
    index = 0
    for url in urls:
        itemsHtml = handleUrl(url)
        index += 1
        print('准备处理%d个url' % index)
        for itemHtml in itemsHtml:
            link, pic, auth = handleHtml(itemHtml)
            dirNum += 1
            saveItem(link[0], pic[0], auth[0])
    print('此次共爬取作品%d个' % (per_page * pageNum))
    print('历史共完成收集作品%d个,下次可设置ordinal值为此数值,可继续爬取' % ordinal)

if __name__ == '__main__':
    main()
