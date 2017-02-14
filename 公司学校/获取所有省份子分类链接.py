'''
阿里巴巴的企业库  慧聪、环球资源，生意宝、中国供应商
http://www.8671.net/
http://hy.qiye.gov.cn/company/
http://xuexiao.chazidian.com/
http://www.xuexiaodaquan.com/
http://xuexiao.51sxue.com/
'''
import requests
from bs4 import BeautifulSoup


def getLinks(url, pro=False, flag=''):  # 控制是否获取主页面源码中连接,处理方法不同
    r = requests.get(url)
    if pro == True:
        r.encoding = 'utf-8'  # 省份解码utf-8乱码
    page = r.text  # 主页面
    soup = BeautifulSoup(page, 'lxml')
    if pro == True:
        ul = soup.find(id='oProvinceIndex')
    else:
        ul = soup.find(id='dCatalogueBox')
    links = ul.find_all('a')
    addrs = []  # 中文+链接地址
    for link in links:
        addr = link.get('href')
        name = flag + link.string
        tmp = [name, addr]
        addrs.append(tmp)
    return addrs


def getProvinces():
    '''返回省份链接'''
    url = 'http://www.8671.net'
    provinces = getLinks(url, True)  # 省分+链接
    return provinces


def getIndustrys(province):
    '''访问省份网页后按分类查询企业'''
    addrs = []  # 所有最小分类链接
    a_industrys = getLinks(province[1])  # 1级分类
    # print(a_industrys)
    for i in a_industrys:
        # print(i[0])
        flag = province[0] + '=>' + i[0] + '=>'
        if i[0] == '国际组织':
            addrs.append(['国际组织', i[1]])
        else:
            b_industrys = getLinks(i[1], flag=flag)  # 2级分类
            # print(b_industrys)
            for j in b_industrys:
                print(j[0])
                c_industrys = getLinks(j[1])  # 3级分类
                addrs.extend(c_industrys)
                # print(addrs)
    return addrs


def saveTxt(addrs):
    tmp = []
    for i in addrs:
        # tmp.append(i[0] + ' : ')
        tmp.append(i[1] + '\n')
    with open('company.txt', 'a', encoding='utf-8') as f:
        f.writelines(tmp)


if __name__ == '__main__':
    provinces = getProvinces()
    # print(provinces)
    # for i in range(9):
    #     del provinces[0]
    for province in provinces:
        links = getIndustrys(province)  # 获取最低级所有分类名称和链接
        #print(links)
        saveTxt(links)
