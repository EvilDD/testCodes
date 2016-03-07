import urllib.parse
import urllib.request

url = 'http://dev.ihaixie.com/shop/index.php?act=member_order&op=addOrder'
data = {
    'u': 'zyd',
    'p': '339c3e65a545716b202144dc5e13601c',
    'pay_sn': '120503764064313006 '
}
params = urllib.parse.urlencode(data).encode(encoding='utf8')
pay_stats = urllib.request.urlopen(url, params)
print(pay_stats.read())
# 目前支付关闭
