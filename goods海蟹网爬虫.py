# -*- coding: UTF-8 -*-
from urllib.request import urlopen
import re
import os

url = 'http://www.ihaixie.com'


class handleHtml():

    """处理html"""

    def __init__(self, url):
        super(handleHtml, self).__init__()
        self.url = url

    '''获取主页面html做初步处理，抓取大段分类商品html'''

    def getHtmls(self, url):
        print('正在尝试打开主人给的网址首页')
        try:
            rep = urlopen(self.url)
            html = rep.read().decode('utf-8')
        except:
            html = '无法获取主页html'
        htmlRule = '<li cat_id="\d+" class="\w+" >(.*?)\r\n\s*</dl>\r\n\s*</div>'
        htmlRe = re.compile(htmlRule, re.S)
        htmls = re.findall(htmlRe, html)
        print('首页html分割若干小的html段落完毕，每段代表一个大类商品')
        return htmls

    '''处理大分类的html获取一级商品分类,返回[(),()]'''

    def getItems1(self, html):
        htmlRule = '<div class="class">\r\n\s*<h4><a href="(.*?)">(.*?)</a>'
        htmlRe = re.compile(htmlRule, re.S)
        items1 = re.findall(htmlRe, html)
        return items1

    '''获取二级商品分类名称,返回[(),()]'''

    def getItems2(self, html):
        htmlRule = '<dt>\r\n\s*<h3><a href="(.*?)">(.*?)</a>'
        htmlRe = re.compile(htmlRule, re.S)
        items2 = re.findall(htmlRe, html)
        return items2

    '''获取三级商品分类名称,返回[[(),()],[(),()]]'''

    def getItems3(self, html):
        htmlRule = 'class="goods-class">\r\n\s*(.*?)\r\n\s*</dd>'
        htmlRe = re.compile(htmlRule, re.S)
        htmls = re.findall(htmlRe, html)
        items3 = []
        for html in htmls:
            item = self.removeAddr(html)
            items3.append(item)
        return items3

    '''去<a href=>标签'''

    def removeAddr(self, html):
        removeAddr = re.compile('<a href="(.*?)">(.*?)</a>')
        items3 = re.findall(removeAddr, html)
        return items3

    '''抓取三级商品页面的html,此时创建creatFolder实类时，
       已创建商品目录并返回三级商品链接页面和三级商品目录'''

    def getGoodsHtml(self):
        folder = creatFolder(self.url)
        links, paths = folder.getLinksCreatFolders()
        index = 0
        pageLinks = []
        pageFloders = []
        for link in links:
            print('准备处理第%d三级商品分类url页面' % (index + 1))
            pageLink = self.handleGoodHtml(link)
            floder = paths[index]
            if len(pageLink) <= 1:
                floder = floder + '/page1'
                pageLinks.append(pageLink[0])
                pageFloders.append(floder)
                if not os.path.exists(floder):
                    os.makedirs(floder)
            else:
                for i in range(len(pageLink)):
                    pageLinks.append(pageLink[i])
                    # print(pageLink[i])
                    i = repr(i + 1)
                    pageFloder = floder + '/page' + i
                    # print(pageFloder)
                    pageFloders.append(pageFloder)
                    if not os.path.exists(pageFloder):
                        os.makedirs(pageFloder)
            index += 1
        return pageLinks, pageFloders

    '''处理返回三级商品目录链接的html'''

    def handleGoodHtml(self, link):
        try:
            rep = urlopen(link)
            goodsHtml = rep.read().decode('utf-8')
        except:
            print('无法获取商品页面')
        rule1 = '下一页</span></a></li><li><a class="demo" href="(.*?)"><span>末页'
        re1 = re.compile(rule1, re.S)
        pageHtml = re.findall(re1, goodsHtml)
        # print(pageHtml[0])
        if pageHtml == []:  # 获取当前页面有几页商品返回每页的url
            pageNum = 1
        else:
            rule = 'curpage=(\d+)'
            rePage = re.compile(rule, re.S)
            pageNum = re.findall(rePage, pageHtml[0])
            pageNum = int(pageNum[0])
        pageUrl = []
        for i in range(pageNum):
            pageStr = str(i + 1)
            tempUrl = link + '&curpage=' + pageStr
            pageUrl.append(tempUrl)
        return pageUrl


class creatFolder():

    '''创建商品的分类目录，三级目录'''
    '''初始化时创建获取html类并初步获取html'''

    def __init__(self, url):
        super(creatFolder, self).__init__()
        self.url = url
        self.itemClass = handleHtml(self.url)
        self.htmls = self.itemClass.getHtmls(self.url)
        # print(self.htmls[2])

    '''获取1-3级目录名以及层次结构,并返回三级目录名和对应的三级商品链接'''

    def getLinksCreatFolders(self):
        linksthirds = []
        folderthirds = []
        for html in self.htmls:
            items1 = self.itemClass.getItems1(html)
            # print(items1[0][1])
            folder1 = "商品列表/" + items1[0][1]  # 一级商品目录
            if not os.path.exists(folder1):
                os.makedirs(folder1)
            items2 = self.itemClass.getItems2(html)
            items3 = self.itemClass.getItems3(html)
            count = len(items2)
            for i in range(count):
                # print(items2[i][1])
                if '/' in items2[i][1]:  # 替换商品名中的/,对新建目录有影响
                    items2Floder = items2[i][1].replace("/", '&')
                else:
                    items2Floder = items2[i][1]
                # print(items2Floder)
                folder2 = folder1 + '/' + items2Floder  # 二级商品目录
                if not os.path.exists(folder2):
                    os.makedirs(folder2)
                # print(items3[i])
                for j in items3[i]:
                    # print(j[1])
                    linksthirds.append(j[0])
                    if '/' in j[1]:
                        items3Floder = j[1].replace('/', '&')
                    else:
                        items3Floder = j[1]
                    # print(items3Floder)
                    folder3 = folder2 + '/' + items3Floder  # 三级商品目录
                    # 人为输入商品分类操作失误多个(空格)\xa0
                    folder3 = folder3.replace('\xa0', '')
                    # print(folder3)
                    folderthirds.append(folder3)
                    if not os.path.exists(folder3):
                        os.makedirs(folder3)
        print('创建商品三级目录完毕')
        return linksthirds, folderthirds

'''抓取当前三级分类下的所有分页的商品链接'''


def getGoodsLinks(pageLink):
    try:
        rep = urlopen(pageLink)
        html = rep.read().decode('utf-8')
    except:
        print('无法打开对应分类分页链接')
    rule = '<div class="goods-name"><a href="(.*?)"'
    rePre = re.compile(rule, re.S)
    goodsLinks = re.findall(rePre, html)
    return goodsLinks


def getImages(goodlink, imgpath):

    try:
        rep = urlopen(goodlink)
        html = rep.read().decode('utf-8')
    except:
        print('无法打开对应商品链接')
    rule = "levelD : '(.*?)'"
    reCom = re.compile(rule, re.S)
    imgsLink = re.findall(reCom, html)
    if imgsLink == []:
        print('发现一枚无效商品链接:%s' % goodlink)
    else:
        index = 0
        for link in imgsLink:
            indexStr = repr(index + 1)
            imgPath = imgpath + '/' + indexStr + '.jpg'
            print(imgPath)  # 打印当前准备获取图片路径
            try:
                conn = urlopen(link)
                f = open(imgPath, 'wb')
                f.write(conn.read())
                f.close()
            except Exception as e:
                print('获取图片时失败', e)
            index += 1


def main():
    html = handleHtml(url)
    pageLinks, pageFloders = html.getGoodsHtml()  # 返回的商品三级分类分页链接列表长度应该和pageFloders一致
    print('分页链接数:%d,分页目录数:%d' % (len(pageLinks), len(pageFloders)))
    for i in range(len(pageLinks)):
        print('正在获取%s下的图片' % pageFloders[i])
        goodsLinks = getGoodsLinks(pageLinks[i])
        for j in range(len(goodsLinks)):
            jstr = repr(j + 1)
            imgPath = pageFloders[i] + '/' + jstr
            if not os.path.exists(imgPath):
                os.makedirs(imgPath)
            getImages(goodsLinks[j], imgPath)

if __name__ == '__main__':
    main()
