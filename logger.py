import logging
import logging.handlers
import os

class logfile(object):

    def __init__(self,log_file):
        self.log_file=log_file

    def init_logger(self):
        dir_path=os.path.dirname(self.log_file)
        try:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        except:
            pass

        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=20 * 1024 * 1024, backupCount=10)
        fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        formatter = logging.Formatter(fmt)
        chlr = logging.StreamHandler()  # 输出到控制台的handler
        chlr.setFormatter(formatter)
        handler.setFormatter(formatter)
        logger_instance = logging.getLogger('logs')
        logger_instance.addHandler(handler)
        logger_instance.addHandler(chlr)
        logger_instance.setLevel(logging.DEBUG)
        return logger_instance

if __name__=='__main__':
    a=logfile('a.log').init_logger()
    a.info('sadas ')

