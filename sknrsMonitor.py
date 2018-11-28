#-*- coding:utf-8 -*-
from selenium import webdriver
import threading
from inform import *
import multiprocessing

lock=threading.Lock()
chat=chat()
class monitor(object):
    def __init__(self):
        # self.countrylist=['cn','jp','us','gb']
        self.countrylist=['cn','jp','us']
        self.start_url='https://www.nike.com'
        self.params='/launch'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless')
        self.option.add_argument('lang=zh_CN.UTF-8')
        self.option.add_argument('--disable-gpu') if ENVIRONMENT=='LINUX' else None
        self.option.add_argument('--disable-dev-shm-usage') if ENVIRONMENT=='LINUX' else None
        self.option.add_argument('--no-sandbox') if ENVIRONMENT=='LINUX' else None
        self.option.add_argument('User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"')
        self.web = webdriver.Chrome(chrome_options=self.option)
        self.proxy=webdriver.Proxy()
        # self.option.add_argument("--proxy-server=http://web-proxy.tencent.com:8080")
        self.pictureDirPath=PICTUREPATH
        self.logger=logger
        self.parsePagePicPath=PARSEPAGEPICPATH
        self.getDetailPicPath=GETDETAILPICPATH

    def commitsql(self,sql):
        try:
            lock.acquire(True)
            res=cur.execute(sql).fetchall()
            return res
        finally:
            lock.release()

    def downloadPics(self,urllist,filenamelist):
        '''
        用requests下载图片链接
        :param urllist:图片链接
        :param filenamelist: 商品名称
        :param missinglist: 详情页抓取丢失的商品集合列表
        :return: 下载到本地后的图片路径列表
        '''
        proxy = {'http':'web-proxy.tencent.com:8080','https':'web-proxy.tencent.com:8080'}
        pictures_list=[]
        try:
            os.mkdir(PICTUREPATH)
        except:
            pass

        for url,filename in zip(urllist,filenamelist):
            filename=removeChineseWord(filename)
            if PROXY:
                req=requests.get(url,headers=header,proxies=proxy)
            else:
                req=requests.get(url,headers=header)
            html=req.content
            pictype=url.split('.')[-1]
            filename=filename.replace(' ','_')
            filename=self.pictureDirPath+filename
            filename+='%s.%s'%(str(time.time())[-4:],pictype)
            pictures_list.append(filename)
            with open(filename,'wb') as f:
                f.write(html)
        return pictures_list

    def parsePage(self,country):
        '''
        解析每个国家上新页面的商品列表
        :param country: 国家字段
        :return: 商品链接列表以及相应图片链接列表
        '''
        return getDetail(country)

    def is_element_exist(self, element, type='xpath',single=True,web=None):
        '''
        判断页面中某个元素是否存在
        :param element: xpath 或者 classname
        :param type: xpath 或者 classname
        :param single: 多个还是单个元素
        :param web:
        :return:
        '''
        flag = True
        result = None
        try:
            if type == 'class_name':
                if web is None:
                    result = self.web.find_element_by_class_name(element) if single else self.web.find_elements_by_class_name(element)
                else:
                    result = web.find_element_by_class_name(element) if single else web.find_elements_by_class_name(element)
            elif type == 'xpath':
                if web is None:
                    result = self.web.find_element_by_xpath(element) if single else self.web.find_elements_by_xpath(element)
                else:
                    result = web.find_element_by_xpath(element) if single else web.find_element_by_xpath(element)
            return flag, result
        except:
            flag = False
            return flag, result

    def storeData(self,country,titlelist, productNamelist, fetchedTimelist, pricelist,availablelist, hreflist, piclist, descriptionlist):
        '''
        country作为表名,将链接列表以及图片链接列表存入数据库
        :param country:
        :param href_list:
        :param pic_list:
        :return:
        '''
        data=pd.DataFrame([titlelist, productNamelist, fetchedTimelist, pricelist,availablelist, hreflist, piclist, descriptionlist],index=['title', 'name', 'fetchedTime','price','availableSizes', 'href', 'picture', 'description']).T
        data.to_sql(country,con=conn,if_exists='replace',index=False)

    def insertNewData(self,origindata,newdata):
        for i in newdata:
            origindata.insert(0,i)
        data=pd.DataFrame(origindata,columns=['title', 'name', 'fetchedTime','price','availableSizes', 'href', 'picture', 'description'])
        return data

    def diagnosis(self,country):
        '''
        检测指定的国家页面
        :param country:
        :return: 新品链接
        '''
        # productDict,titlelist,productNamelist,fetchedTimelist,availablelist,hreflist,piclist,descriptionlist
        productDict, titlelist, productNamelist, fetchedTimelist, pricelist,availablelist, hreflist, piclist, descriptionlist=self.parsePage(country)
        if (country,) not in self.commitsql('select name from sqlite_master where type="table"'):
            print('数据库中不存在数据表%s,创建中..'%country)
            print(hreflist)
            self.storeData(country,titlelist, productNamelist, fetchedTimelist, pricelist,availablelist, hreflist, piclist, descriptionlist)
            return
        sql='select name from %s'%country
        origin_name_list=[i[0] for i in self.commitsql(sql)]
        print('%s_origin_name_list:'%country,origin_name_list)
        print('%s_current_name_list:'%country,productNamelist)
        length=len(hreflist)
        new_list=[]
        countrydict = {'cn': '中国', 'us': '美国', 'jp': '日本', 'gb': '英国'}
        for i in range(length):
            if productNamelist[i] not in origin_name_list:
                new_list.append({'title':titlelist[i], 'name':productNamelist[i],'fetchedTime':fetchedTimelist[i], 'price':pricelist[i],'availableSizes':availablelist[i], 'href':hreflist[i], 'picture':piclist[i], 'description':descriptionlist[i]})
        if new_list:
            self.logger.info('----%s新品发售----'%countrydict[country])
            for i in new_list:
                self.logger.info('%s新品%s:%s:'%(countrydict[country],i['name'],i['href']))
            return new_list
        else:
            print('无新品发售')
            return


    def informINFO(self,country,new_list):
        '''
        访问新商品详情页并获取相应的详情数据以及下载相应图片至本地,并调用inform.py发送微信通知
        :param country:
        :param new_list:
        :return:
        '''
        try:
            os.mkdir('NewPics')
        except:
            pass
        #'title', 'name', 'fetchedTime', 'availableSizes', 'href', 'picture', 'description'
        titlelist=[i['title'] for i in new_list]
        namelist=[i['name'] for i in new_list]
        fetchedTimelist=[i['fetchedTime'] for i in new_list]
        pricelist=[i['price'] for i in new_list]
        availablelist=[i['availableSizes'] for i in new_list]
        urlist=[i['href'] for i in new_list]
        pictureslist=[i['picture'] for i in new_list]
        descriptionlist=[i['description'] for i in new_list]

        LocalPicturesPathList = self.downloadPics(pictureslist, titlelist)


       # 构造新品列表
        newdatalist=[]
        for i in zip(titlelist,namelist,fetchedTimelist,pricelist,availablelist,urlist,pictureslist,descriptionlist):
            newdatalist.append(i)

        # 将新品插入原始数据中
        origindatalist=self.commitsql('select * from %s' % country)

        newdata=self.insertNewData(origindatalist,newdatalist)
        newdata.to_sql(country,conn,index=False,if_exists='replace')

        self.logger.info('infolist'+repr(new_list).replace('\xae',''))
        self.logger.info('pictureslist'+repr(pictureslist))

        # 发信息通知
        informtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        try:
            chat.sendmsg(country,informtime,newdatalist,LocalPicturesPathList)
        except Exception as e:
            self.logger.info(e)
            self.logger.info('微信信息发送失败,数据库回滚')
            hreflist = cur.execute('select href from %s' % country).fetchall()
            missingList=[hreflist.index((i,)) for i in urlist]
            datalist = cur.execute('select * from %s' % country).fetchall()
            rml = [datalist[i] for i in missingList]
            for i in rml:
                logger.info('send msg failed,remove '+ repr(i)+ ' from database')
                datalist.remove(i)
            datalist=pd.DataFrame(datalist,columns=['title', 'name', 'fetchedTime','price','availableSizes', 'href', 'picture', 'description'])
            datalist.to_sql(country,conn,if_exists='replace',index=False)

        return newdatalist,LocalPicturesPathList

    def check_login_status(self,interval):
        '''
        检查登录状态
        :param interval:
        :return:
        '''
        while True:
            if not chat.bot.is_listening:
                logger.info('已掉线,重新登录')
                chat.login()
                self.logger.info('已重新登录')

            else:
                time.sleep(interval)


    def start(self):
        '''
        :return:
        '''
        print('新品通知将发送到:',CHATROOMNAMELIST)
        threading.Thread(target=self.check_login_status,args=(6,)).start()  #另外开启线程保持检查微信登录状态
        while True:
            try:
                countrylist=self.countrylist
                for country in countrylist:
                    new_list=self.diagnosis(country)
                    if new_list:
                        infolist,pictures_list=self.informINFO(country,new_list)
                    random_sleep()
            except Exception as e:
                self.logger.info('Error occurred %s'%e)
                pass

    # def start1(self,country):
    #     while True:
    #         print('检测%s'%country)
    #         new_list = self.diagnosis(country)
    #         if new_list:
    #             infolist, pictures_list, urlist = self.informINFO(country, new_list)
    #             try:
    #                 # chat.sendmsg(country,infolist,pictures_list,urlist)
    #                 pass
    #             except Exception as e:
    #                 self.logger.info(e)
    #                 self.logger.info('微信信息发送失败,数据库回滚')
    #                 datalist=self.commitsql('select * from %s' % country)
    #                 # datalist = cur.execute('select * from %s' % country).fetchall()
    #                 hreflist=[(i[0],) for i in datalist]
    #                 missingList=[hreflist.index((i,)) for i in urlist]
    #                 rml = [datalist[i] for i in missingList]
    #                 for i in rml:
    #                     logger.info('send msg failed,remove '+ repr(i)+ ' from database')
    #                     datalist.remove(i)
    #                 rm_href_list = [i[0] for i in datalist]
    #                 rm_name_list = [i[1] for i in datalist]
    #                 self.storeData(country, rm_href_list, rm_name_list)
    #         random_sleep()

    # def main(self):
    #     print('新品通知将发送到:', CHATROOMNAMELIST)
    #     # threading.Thread(target=self.check_login_status, args=(6,)).start()  # 另外开启线程保持检查微信登录状态
    #     for country in self.countrylist:
    #         t=threading.Thread(target=self.start1,args=(country,))
    #         t.setDaemon(True)
    #         t.start()

if __name__=='__main__':

    test=monitor()
    # test.parsePage()
    # test.start()
    # l=[{'href':'https://www.nike.com/cn/launch/t/air-jordan-1-nrg-sail-varsity-red-black/','pic':'https://c.static-nike.com/a/images/w_960,c_limit,f_auto/bwa1irquryzwwffnyp0w/nrg.jpg'},{'href':'https://www.nike.com/cn/launch/t/air-max-deluxe-blue-force-total-orange/','pic': 'https://c.static-nike.com/a/images/t_prod_ss/w_960,c_limit,f_auto/bof7z8rpkdskjobpoauh/life-of-the-party.jpg'}]
    # l=[{'href':'https://www.nike.com/jp/launch/t/nike-air-foamposite-pro-black-metallic-gold/','pic':'https://c.static-nike.com/a/images/t_prod_ss/w_960,c_limit,f_auto/zy9vkmmnobh3ufurut5x/blackmetallic-gold.jpg'}]
    # test.informINFO('jp',l)
    # web=webdriver.Chrome()
    # web.get('https://www.nike.com/gb/launch/')
    # test.parseErrorPage('https://www.nike.com/gb/launch/t/air-jordan-11-concord-white-black/',web)
    # test.main()


    # threading.Thread(target=self.check_login_status, args=(6,)).start()  # 另外开启线程保持检查微信登录状态
    # pool=multiprocessing.Pool()
    # for country in test.countrylist:
    #     pool.apply(test.start1,args=(country,))
    # pool.close()
    # pool.join()
    test.start()
