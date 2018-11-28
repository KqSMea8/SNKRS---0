import random
import urllib.request
from config import *

proxy = {'http': 'web-proxy.oa.com:8080', 'https': 'web-proxy.oa.com:8080'}

USERAGENT=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
           'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
           'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729',
           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
           'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
           ]

'''
Restricted 	bool		专属购买
Publisheddate	时间	上新时间？？
SeoSlug			产品链接
Imageurl		封面图片链接
	Title 名字
SelectionEngine	DAN:抽签	LEO：限量	FLOW：先到先得
Merchstatus 		预警？？
Skus/items/localizedSize	码数 bool
Available 		bool		是否可购买
Upcoming	 bool	是否即将上架
Colordescription	中文颜色描述
Restricted 	bool		专属购买
Publisheddate	时间	上新时间？？
SeoSlug			产品链接
Imageurl		封面图片链接
	Title 名字
SelectionEngine	DAN:抽签	LEO：限量	FLOW：先到先得
Merchstatus 		预警？？
Skus/items/localizedSize	码数 bool
Available 		bool		是否可购买
Upcoming	 bool	是否即将上架
Colordescription	中文颜色描述
'''

'''
用多个账号构建多个headers
'''
header={
    'Host': 'api.nike.com',
    'Content-Type':'application/json',
    'Accept':'*/*',
    'X-acf-sensor-data': '1,i,t/S4MVh/1ay75qLwZ1ntAE4EpCb9lNhHV6rgnEUPydGfhmLVETTm+KLW34CxNsuuDmRsPUjdLDz2slnwiuXrmNKAXKQk5i7zPhPB/Hd0l2j2r05bNdq7KU0/jfiSLJ8Vw28aiqBnVOg8gUaqPDDRFVqd+mhFaHazn5mq/5TqD+o=,I8miP15h14Ixww4COYSzdG+JfhgyBixkgFajbk+F4ophM1nirGBVRzYa4mfYCa6Tm73oRJIXsvA/LPJvTjdADQLB4JIpZqNe43L05tj7yTizyUM2Yv5MZuntWbfzP8F+etQPAFbjMOxAby7zDL8JYu3IIRWmoK3AbcEMy5qcLLc=$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$12,4,18',
    'Cookie':'abck=59935F5EB3F8061A524BC2DE3EF39C3F~-1~YAAQZcU8twrdhjpnAQAAu55sVACCrocy7Wn0erGmx3WVwtHYFCjpc4EH7VaKekTtSWMlAPivqFBeFq4s8OYF0obAcGfE3r+1jFFPsNhMXoKYPJPAZlW3xsKjN15TlRYwOrQydezI5rJoByAslk0XBmQvuEXr7oPd7o0Se4k8itM+IyBIcnI+hGRjS4h/lJt3LEDRZUBUxAAcTJ55goV+Z9F1zLePqNhmgo6S7+cadfPODNdk2lD8/PSQgMTnE/nUNZ9JGIoaT9mBiSRsjSNfEu4zQdYXaWKUZ10=~-1~-1~-1; bm_sz=5CF5D3C6243AF88B19FF5E365E4C2713~QAAQZcU8twndhjpnAQAAu55sVAlM5lBWKIo1DsWufuLbPTg061pgV8cqd2Hzn7DOQJnxeWffJ2yfu3ndVUH7CXa0G82n1DZ9jyLKUmLvVXn/ENGiMnLRUUT8d8pJ/DUWITeFjQi4yPv7nxCa0MtkShMGk0wiSz0BvZ+kPiefwHnixQG1ALkYCHWTrBoE',
    'Connection': 'keep-alive',
    'X-NewRelic-ID': 'VQYGVF5SCBADUVBRBgAGVg==',
    'User-Agent': 'SNKRS/3.7.0 (iPhone; iOS 12.0.1; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, zh-Hant-HK;q=0.9, ja-JP;q=0.8',
    'Authorization': 'BearereyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2YWI1NThkLWMwZTMtNGVhYi05MTljLTJkYjA3YjFjN2NhMHNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE1NDMzMjQwMDQsImV4cCI6MTU0MzMyNzYwNCwiaXNzIjoib2F1dGgyYWNjIiwianRpIjoiYjk0NmU4ZjQtZjc4Ni00YzcyLWE3MTMtYzkwMDAyNDYxMzZiIiwibGF0IjoxNTQzMzA5NzgxLCJhdWQiOiJjb20ubmlrZS5kaWdpdGFsIiwic3ViIjoiY29tLm5pa2UuY29tbWVyY2Uuc25rcnMuaW9zIiwic2J0IjoibmlrZTphcHAiLCJzY3AiOlsiY29tbWVyY2UiXSwicHJuIjoiODY2YTlmM2ItYWZlNS00NTEwLTliMDAtMGU0ZDAxZmJlNzg3IiwicHJ0IjoibmlrZTpwbHVzIn0.Xf4XJ5Z2rrdoZenvyEpn2CFliEtZyZEDEUcVxTFaVcz6GIrKMZq3dc-ir7i3AolKdYVyUeyFkraSgw2rz_yVLF8BUJ7f23i_J9XZUCt_sZ6MMdpzBF2S1ZcwkaBclTqrvD3uZ_au4swafL84hmzmCCmeCWEFAkj39A0A7QCZ46rSslQIsYGFAStRlcM1lILv8wPBeRDJ_jHfIfMHz3kTjoOoJX7o5ONy4wH4TmckYh9F6IqtY5XQHi0G61dQ_heHMFQPQwhgn7URVHIrWsde-EGgblmaWd2h25OLTWK-GHNRhXR68O5LbkVMhop5r9MGYGUrBE7BLytwwKNNHP4sUw'
}

url='https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published'

def get_html():
    try:
        if PROXY:
            httpproxy_handler = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(httpproxy_handler)
            request = urllib.request.Request(url,headers=header)
            response = opener.open(request)
        else:
            request = urllib.request.Request(url, headers=header)
            response=urllib.request.urlopen(request)
        return response.read().decode('utf-8')
    except:
        return ""

# req=urllib.request.Request(url,headers=header)
# res=urllib.request.urlopen(req)
# s=res.read()
# print(type(s))
# print(s.decode('utf-8'))
# print(s.decode('unicode-escape'))