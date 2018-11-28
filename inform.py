# coding:utf-8
from wxpy import *
from util import *


class chat(object):
    def __init__(self):
        self.bot = Bot(cache_path=True,console_qr=CONSOLEQR)

    def login(self):
        self.bot = Bot(cache_path=True,console_qr=CONSOLEQR)

    def logout(self):
        self.bot.logout()

    def sendmsg(self,country,informtime,infolist,piclist):
        user=self.bot.self
        countrydict={'cn':'中国','us':'美国','jp':'日本','gb':'英国'}
        for (title,name,fetchedTime,price,availableSizes,url,_,description),pic in zip(infolist,piclist,):
            for chatname in CHATROOMNAMELIST:
                chatroom=self.bot.groups().search(chatname)[0]
                message='''【%s】新品：%s\n价格：%s\n可选鞋码:%s\n商品链接:%s\n程序更新时间:%s\n官网更新时间:%s\n------------------------------------\n介绍:%s'''%(countrydict[country],title,price,availableSizes,url,informtime,fetchedTime,description)
                logger.info(country+','+countrydict[country]+','+url)
                if country =='us' and ('cn' in url or 'jp' in url):
                    logger.info('美国商品数据库遭其他国家商品传入,删除数据库')
                    cur.execute('drop table us')
                    user.send('注意:美国商品数据库遭其他国家商品传入')
                    break
                if country=='cn' and 'cn' not in url:
                    logger.info('中国商品数据库遭其他国家商品传入,删除数据库')
                    cur.execute('drop table cn')
                    user.send('注意:中国商品数据库遭其他国家商品传入')
                    break
                if country=='jp' and 'jp' not in url:
                    logger.info('日本商品数据库遭其他国家商品传入,删除数据库')
                    cur.execute('drop table jp')
                    user.send('注意:日本商品数据库遭其他国家商品传入')
                    break
                # self.chatroom.send_image(pic)
                # self.chatroom.send(message)
                print(message)
                print(pic)
                flag=checkIfRepeat(country,url,name,chatname)
                if SELFTEST:
                    flag=True
                if flag :
                    try:
                        os.chdir(PICTUREPATH)
                        chatroom.send_image(pic) if not SELFTEST else user.send_image(pic)
                    except:
                        # self.logger.info('%s send failed'%pic)
                        chatroom.send_image('snkrs.jpg') if not SELFTEST else user.send_image('snkrs.jpg')
                    chatroom.send(message) if not SELFTEST else user.send(message)
                    time.sleep(random.randint(10,20)/10.0)
                os.chdir(WORKPATH)

if __name__=='__main__':
    test=chat()
    country='cn'
    href='https://www.nike.com/cn/launch/t/air-jordan-1-double-strap-white-black-dark-concord/'
    # infolist=[{'productName': '男子运动鞋 AIR JORDAN 1 RE HI DOUBLE STRP', 'price': '￥1,199', 'date': '-'}, {'productName': '男子运动鞋 AIR JORDAN 1 RE HI DOUBLE STRP', 'price': '￥1,199', 'date': '-'}]
    # piclist=['E:\\NewPics\AIRJORDANREHIDOUBLESTRP6667.jpg', 'E:\\NewPics\AIRJORDANREHIDOUBLESTRP9583.jpg']
    # urllist=['https://www.nike.com/cn/launch/t/air-jordan-1-double-strap-white-black-dark-concord/', 'https://www.nike.com/cn/launch/t/air-jordan-1-double-strap-gym-red-white-sail/']
    # test.sendmsg(country,infolist,piclist,urllist)
    # test.checkIfRepeat(country,href,'SNKRS测试群')
