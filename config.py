import os

# ENVIRONMENT='LINUX'
ENVIRONMENT= 'WINDOWS'
CONSOLEQR=False
SELFTEST=False
PROXY=False

DBPATH = 'SNKRS.db'
LOGDB= 'SNKRSLOG.db'
WORKPATH='F:\python_project\SNKRS\\' if ENVIRONMENT=='WINDOWS' else '/root/project/snkrs'
BACKUPDBPATH=os.getcwd()+r'\backup\\'
PARSEPAGEPICPATH=os.getcwd()+r'\ParsePagePic\\' if ENVIRONMENT == 'WINDOWS' else os.getcwd() + r'/ParsePagePic//'
GETDETAILPICPATH=os.getcwd()+r'\GETDETAILPIC\\' if ENVIRONMENT == 'WINDOWS' else os.getcwd() + r'/GETDETAILPIC//'
PICTUREPATH=r'E:\NewPics\\' if ENVIRONMENT == 'WINDOWS' else os.getcwd() + r'/NewPics//'
BACKUPDB=BACKUPDBPATH+'backup_%s_LOGDB.db'
LOGFILE='SNKRS.log'


# CHATROOMNAMELIST=['SNKRS测试群','SNKRS测试2']
CHATROOMNAMELIST=['SNKRS测试群']
# CHATROOMNAMELIST=['JUST DROPPED']
# CHATROOMNAMELIST=['FOMO监控二群']
# CHATROOMNAMELIST=['FOMO监控一群（禁聊）','JUST DROPPED']
# CHATROOMNAMELIST=['FOMO监控一群（禁聊）','FOMO监控二群（禁聊）','JRs球鞋信息共享群','SNKRS测试群','SNKRS测试2']

