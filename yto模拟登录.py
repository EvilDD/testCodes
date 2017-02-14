# -*- coding:utf-8 -*-
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
import json
import re
import time

# url = 'http://ewms.yto56.net.cn/toLogin.action'  # 登录页面需要验证码
urlLogin = 'http://ewms.yto56.net.cn/doLogin.action'  # post数据页面
urlM = 'http://ewms.yto56.net.cn/searchWarnInfoManage.action?currentPage=1&menuFlag=dzmd_dzmd'  # 面单详情页面
urlMD = 'http://ewms.yto56.net.cn/searchWarnInfoManage.action?userName=K89354469'  # 面单post数据页面
userName = 'K89354469'
passWord = 'Yoursender_2016a'
headers = {
    'Host': 'ewms.yto56.net.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive'
}


def getCookieLogin():
    # 第一次访问,lwpCookieJar是CookieJar的派生类可保存到cookie.txt
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.LWPCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    try:
        rep = urllib.request.urlopen(urlLogin, timeout=5)
        print('进入登录页面')
    except BaseException as e:
        print('登录页面未正确打开:', e)
    # print('First', rep.info())

    # 第二次访问post数据，cookie已经带上
    postData = {
        'userName': userName,
        'userPassword': passWord,
        'codeString': '',
        'isRemeber': '1'
    }
    data = urllib.parse.urlencode(postData).encode('utf-8')
    req = urllib.request.Request(urlLogin, data, headers=headers)
    try:
        print('尝试登录')
        rep = urllib.request.urlopen(req, timeout=5)
        html = rep.read().decode('utf-8')
    except BaseException as e:
        html = ''
        print('数据未正确postg到login页面:', e)
    reCom = re.compile('面单详情', re.S)
    isLogin = re.search(reCom, html)
    # cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
    # print('Second:', rep.info())
    # 可循环打印出cookie的名字和对应值
    # for item in cookie:
    #     print('Name = ' + item.name)
    #     print('Value = ' + item.value)
    return isLogin


def getMdData():
    # 第三次直接获取面单面页面数据
    isDate = False
    while not isDate:
        Sdate = input('输入起始时间格式如2016-1-16:')
        Edate = input('输入结束时间格式如2016-1-16:')
        isDate = checkDate(Sdate, Edate)
    postData = {
        'materialCode': 'DZ100301',
        'partiondateStart': Sdate,
        'partitiondateEnd': Edate,
        'userCode': 'K200221738'
    }
    data = urllib.parse.urlencode(postData).encode('utf-8')
    req = urllib.request.Request(urlMD, data, headers=headers)
    req.add_header('Referer', urlM)
    try:
        req = urllib.request.urlopen(req, timeout=5)
        info = req.read().decode('utf-8')
    except urllib.error.URLError as e:
        print('面单post页面打开失败', e)
    info = json.loads(info)
    print(('商家面单号统计:\n总数量:%d已使用:%d未使用:%d') %
          (info['total'], info['useNumber'], info['notUseNumber']))


def checkDate(StartDate, EndDate):
    rule = re.compile('^\d{4}-\d{1,2}-\d{1,2}$')
    isFormat = re.match(rule, StartDate)
    if isFormat is not None:
        isFormat = re.match(rule, EndDate)
        if isFormat is None:
            print('输入结束时间格式不正确')
            return False
    else:
        print('输入起始时间格式不正确')
        return False
    timeAarry1 = time.strptime(StartDate, '%Y-%m-%d')
    stamp1 = time.mktime(timeAarry1)
    timeAarry2 = time.strptime(EndDate, '%Y-%m-%d')
    stamp2 = time.mktime(timeAarry2)
    if stamp1 >= stamp2:
        print('起始时间应该小于结束时间')
        return False
    nowTime = float(time.time())
    # print(nowTime, stamp1, stamp2)
    if stamp1 > nowTime or stamp2 > nowTime:
        print('输入的日期大于当前日期')
        return False
    return True


def main():
    isLogin = getCookieLogin()
    if isLogin is not None:
        print('登陆成功')
        getMdData()
    else:
        print('登陆失败')

if __name__ == '__main__':
    main()
# f = open('html1.txt', 'w', encoding='utf-8')
# f.write(html)
# f.close()
