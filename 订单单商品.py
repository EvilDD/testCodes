import urllib.parse
import urllib.request

url = 'http://dev.ihaixie.com/shop/index.php?act=member_order&op=addOrder'
data = {
    'u': 'zyd',
    'p': '339c3e65a545716b202144dc5e13601c',
    'o[0][reference_number]': '112246',
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
params = urllib.parse.urlencode(data)
# params为字节类型
params = params.encode(encoding='utf-8')
add_order = urllib.request.urlopen(url, params)
# 字节转字符串
add_order = str(add_order.read(), encoding='UTF-8')
print(add_order)
