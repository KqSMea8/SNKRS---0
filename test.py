from selenium import webdriver
import multiprocessing
import time
def we():
    w=webdriver.Chrome()
    print('saddq')
    w.get('https://www.nike.com/launch/')
    time.sleep(3)
    w.close()

def process(num):
    print('Process:', num)

if __name__ == '__main__':
    for i in range(3):
        p = multiprocessing.Process(target=we, args=())
        p.start()