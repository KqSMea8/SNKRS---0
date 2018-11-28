'''
构建本地SNKRSLOG.db
直接单独运行即可
目的:
另外构建SNKRSLOG.db存储已发送信息,避免重新发送旧商品到群中,数据库信息包括:
表名country:
    productname
    href
    time
    chatroom
运行程序时留意config文件中的CHATROOMLIST,数据库将标记这些群全部为已发送
'''
import sqlite3
from config import *
import pandas as pd
import time
chatroomlist=CHATROOMNAMELIST
def mklogdb():
    con1=sqlite3.connect(DBPATH)
    cur1=con1.cursor()
    con2=sqlite3.connect(LOGDB)
    cur2=con2.cursor()
    countrylist=['cn','jp','us']
    for country in countrylist:
        datalist=cur1.execute('select href,name from %s'%country).fetchall()
        hreflist=[i[0] for i in datalist]
        productNamelist=[i[1] for i in datalist]
        # print(hreflist)
        # print(productNamelist)
        data=pd.DataFrame([productNamelist,hreflist]).T
        data['time']=time.ctime()
        data.columns=['productName','href','time']
        tmp=[data.copy() for i in range(len(chatroomlist))]
        tmp2=pd.DataFrame()
        for index,chatroom in enumerate(chatroomlist):
            tmp[index]['chatroom']=chatroom
        # print('------',country,'----------')
        # print(tmp)
        for i in tmp:
            tmp2=tmp2.append(i)
        # print(tmp2)
        data=tmp2
        # print(data)
        data.to_sql(country,con2,if_exists='replace',index=False)
    res=cur2.execute('select * from %s'%'cn').fetchall()
    for i in res:
        print(i)
mklogdb()