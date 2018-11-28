import requests
import time
import random
from config import *
from logger import *
from shutil import copyfile
import sqlite3
import pandas as pd
from datetime import datetime
import re
from RequestsConfig import *
import urllib.request

logger = logfile(LOGFILE).init_logger()
proxy = {'http': 'web-proxy.oa.com:8080', 'https': 'web-proxy.oa.com:8080'}
header={}

con_log = sqlite3.connect(LOGDB,check_same_thread=False)
cur_log = con_log.cursor()
conn=sqlite3.connect(DBPATH,check_same_thread=False)
cur=conn.cursor()

# def get_html(url):
#     try:
#         user_agent = USERAGENT[random.randint(0, len(USERAGENT))]
#         header['User-Agent'] = user_agent
#         if PROXY:
#             response = requests.get(url=url, headers=header,proxies=proxy)
#         else:
#             response = requests.get(url=url, headers=header)
#         return response.text
#     except:
#         return ""

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


def random_sleep():
    time.sleep(random.randint(4000,9000)/1000.0)

def removeChineseWord(words):
    '''
    保存图片时,将图片名中的中除去英文以外的字符去除
    以存在非英文字符的命名的图片发送微信存在报错情况
    :param words: 传入的原字符串
    :return: 剔除非英文字符后的字符串
    '''
    tmp=[]
    words=list(words)
    for word in words:
        if not( chr(65) <= word <= chr(90) or chr(97) <= word <= chr(122)):
            continue
        else:
            tmp.append(word)
    return ''.join(tmp)


def utc2local( utc_time ):
    # UTC 时间转本地时间（ +8:00 ）
    tmp1=utc_time.split('T')[0].split('-')
    year=int(tmp1[0])
    month=int(tmp1[1])
    day=int(tmp1[2])
    tmp2=utc_time.split('T')[1].split('.')[0].split(':')
    hour=int(tmp2[0])
    minute=int(tmp2[1])
    second=int(tmp2[2])
    dt=datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second)
    local_tm = datetime.fromtimestamp(86400)
    utc_tm = datetime.utcfromtimestamp(86400)
    offset = local_tm - utc_tm
    fetchedtime=dt+ offset
    return datetime.strftime(fetchedtime,'%Y-%m-%d %H:%M:%S')

def getSizeRun(data,item):
    sizecode = {}
    itemdata=data['product']['availabilities']['data']['items'][item]
    for i in itemdata['sizes']:
        sizecode[i] = itemdata['sizes'][i]['localizedSize'].replace('EU ','')+'码'
    size=itemdata['sizeRun']
    AvailableSize=[i.replace(i.split(':')[0], sizecode[i.split(':')[0]]).replace(':y', '') for i in size.split('|') if i.split(':')[1] == 'y']
    return  '|'+''.join([i + '|' for i in AvailableSize]) if AvailableSize else '暂无可选购码数'

# def getDetail(country):
#     url='https://www.nike.com/'+country+'/launch/'
#     html=get_html(url)
#     while not html:
#         print('网页获取失败,重新抓取')
#         random_sleep()
#         html = get_html(url)
#     p=re.compile('<script>window.__PRELOADED_STATE__ = (.*?)</script>')
#     # data 字符处理
#     null=''
#     true=True
#     false=False
#     data=eval(p.findall(html)[0])
#     # print(data)
#
#     items = data['product']['threads']['data']['items']
#     itemslist=[*items]
#     productDict={}
#     titlelist = []
#     productNamelist=[]
#     piclist = []
#     hreflist=[]
#     descriptionlist=[]
#     fetchedTimelist=[]
#     availablelist=[]
#     pricelist=[]
#
#     for item in items:
#         dflag=0
#         pflag=0
#         description=''
#         fetchedTime=utc2local(items[item]['_fetchedAt'])
#         fetchedTimelist.append(fetchedTime)
#         title=items[item]['cards'][0]['title']+items[item]['cards'][0]['subtitle'] if items[item]['cards'][0]['title'] != '' else '---*VIP专属购买*---'+items[item]['seo']['slug'].upper().replace('-',' ')
#         productName=items[item]['seo']['slug']
#         picturehref=''
#
#         for card in items[item]['cards']:
#             if card['subType']=='image' and pflag==0:
#                 picturehref = card['defaultURL']
#                 pflag+=1
#             else:
#                 if pflag==0:
#                     for c in card['cards']:
#                         if c['subType'] == 'image' and pflag == 0:
#                             picturehref = c['defaultURL']
#                             pflag += 1
#             if card['subType']=='carousel' and dflag==0:
#                 dp = re.compile('<p>(.*?)</p>')
#                 tmp=card['description'].replace('\n',';').replace('<br>','')
#                 description = dp.findall(tmp)[0]
#                 dflag += 1
#
#         productId = items[item]['productIds'][0] if items[item]['productIds'] else ''  # 多个款型取第一个
#
#         pricedata=data['product']['products']['data']['items']
#         price = pricedata[productId]['currency']+' '+str(pricedata[productId]['currentPrice']) if productId else '-'
#         size = getSizeRun(data,productId) if productId else '无可购选码数'
#         href = 'https://www.nike.com/' + country + '/launch/t/' + items[item]['seo']['slug']
#         description = description if description else '-'
#
#
#         hreflist.append(href)
#         pricelist.append(price)
#         descriptionlist.append(description)
#         piclist.append(picturehref)
#         productNamelist.append(productName)
#         titlelist.append(title)
#         availablelist.append(size)
#
#         productDict[productName]={}
#         productDict[productName]['title']=title
#         productDict[productName]['picture']=picturehref
#         productDict[productName]['description']=description
#         productDict[productName]['productId']=productId
#         productDict[productName]['href']=href
#         productDict[productName]['availableSize']=size
#
#     return productDict,titlelist,productNamelist,fetchedTimelist,pricelist,availablelist,hreflist,piclist,descriptionlist

def getDetail(country):
    pass

def checkIfRepeat( country,href,name,chatroom):
    '''
    检查是否重复
    有的商品链接可能会发生改变,但商品名不变
    :param country:
    :param href:
    :return:
    '''
    try:
        os.mkdir(BACKUPDBPATH)
    except:
        pass
    os.chdir(WORKPATH)
    productName=name
    data=cur_log.execute('select * from %s'%country).fetchall()
    productAndhrefAndRoom=[(i[0],i[3]) for i in data]
    try:
        pos=productAndhrefAndRoom.index((productName,chatroom))
        date=data[pos][2]
        if (productName,chatroom) in productAndhrefAndRoom:
            logger.info('%s ALREADY SENT YET AT %s to %s'%(productName,date,chatroom))
            return False
    except:
        data.insert(0,(productName,href,time.ctime(),chatroom))
        new_data=pd.DataFrame(data,columns=['productName','href','time','chatroom'])
        new_data.to_sql(country,con_log,if_exists='replace',index=False)
        copyfile(LOGDB,BACKUPDB%time.time())
        return True