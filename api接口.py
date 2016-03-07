# -*- coding:utf-8 -*-
import urllib.parse
import urllib.request
# from urllib import request, parse
# request.urlopen()
url = 'http://dev.ihaixie.com'
data = {'u': 'zyd', 'p': '339c3e65a545716b202144dc5e13601c'}

# 返回api的url和参数


def api_method(action):
    global url
    global data
    temp_data = {}
    if action == 'add_order_one':
        url = url + '/shop/index.php?act=member_order&op=addOrder'
        temp_data = {
            "o[0][reference_number]": "1992",
            'o[0][reciver_name]': '周东',
            'o[0][reciver_id_number]': '42011419861026511X',
            'o[0][reciver_mobile]': '13222222222',
            'o[0][reciver_tel]': '0755-123456',
            'o[0][shipping_fee]': '10',
            'o[0][shipping_type]': 'SF',
            'o[0][postcode]': '518100',
            'o[0][province]': '湖北省',
            'o[0][city]': '武汉市',
            'o[0][county]': '江汉区',
            'o[0][address]': '深南大道123号',
            'o[0][sender_name]': '天虹网上商城',
            'o[0][sender_tel]': '4001840018',
            'o[0][goods_serial]': '3963045NA-B',
            'o[0][goods_num]': '1',
            'o[0][customs_goods_price]': '490'
        }
    elif action == 'add_order_more':
        url = url + '/shop/index.php?act=member_order&op=addOrder'
        temp_data = {
            "o[0][reference_number]": "1994",
            'o[0][reciver_name]': '周东',
            'o[0][reciver_id_number]': '42011419861026511X',
            'o[0][reciver_mobile]': '13222222222',
            'o[0][reciver_tel]': '0755-123456',
            'o[0][shipping_fee]': '10',
            'o[0][shipping_type]': 'SF',
            'o[0][postcode]': '518100',
            'o[0][province]': '湖北省',
            'o[0][city]': '武汉市',
            'o[0][county]': '江汉区',
            'o[0][address]': '深南大道123号',
            'o[0][sender_name]': '天虹网上商城',
            'o[0][sender_tel]': '4001840018',
            'o[0][goods_serial]': '3963045NA-B',
            'o[0][goods_num]': '1',
            'o[0][customs_goods_price]': '490',
            "o[1][goods_serial]": "8809241885580",
            "o[1][goods_num]": "1",
            "o[1][customs_goods_price]": "490"
        }
    elif action == 'pay_order':
        url = url + '/shop/index.php?act=member_order&op=payOrder'
        # 支付单号
        temp_data = {'pay_sn': '300504014252437006'}
    elif action == 'order_statu':
        url = url + '/shop/index.php?act=member_order&op=getOrderStatus'
        # 订单编号reference_number
        temp_data = {'o': '1994'}
    elif action == 'stock':
        url = url + '/shop/index.php?act=goods&op=getstock'
        temp_data = {"s": '3963045NA-B'}
    else:
        return "Don't have api interface !"
    data.update(temp_data)
    data = urllib.parse.urlencode(data).encode('utf8')
    return url, data

# get或post提交


def web_method(method, url, data):
    if method == 'get':
        data = str(data, encoding='utf8')
        p_url = url + '&' + data
        rep = urllib.request.urlopen(p_url)
        api_con = rep.read()
        return api_con
    elif method == 'post':
        req = urllib.request.Request(url, data)
        rep = urllib.request.urlopen(req)
        api_con = rep .read()
        return api_con


def main():
    # add_order_one,add_order_more,pay_order,order_statu,stock
    url, data = api_method('pay_order')
    api_con = web_method('post', url, data)
    print(api_con.decode('utf-8'))

if __name__ == '__main__':
    main()
