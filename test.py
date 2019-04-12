from selenium import webdriver
import multiprocessing
from setting import *









def test(url,driver):
    driver.get(url)
    html=driver.page_source
    print(driver.title)
    # with open("%s.html"%url,'a',encoding='utf-8') as f:
    #     f.write(html)
    #     print(url,'写入完成!')
    return html


def re_driver():
    driver=webdriver.Chrome(CHROME_PATH)
    print("启动中!")
    return driver




def mul():
    p=multiprocessing.Pool(3)
    url_list = ['https://www.baidu.com', 'https://www.daweijita.com', 'https://www.amazon.com']
    driver=re_driver()
    for rankBY in url_list:  # data 是要多进程处理的参数
        p.apply_async(test, args=(rankBY,driver))
    print('正在多进程抓取写入第goods层链接')
    p.close()
    p.join()
    print('第goods层链接写入完成!')
    print("line to mysql..")
    driver.quit()

if __name__ == '__main__':
    # mul()
    driver=re_driver()
    for url in ['https://www.baidu.com', 'http://www.daweijita.com', 'https://www.amazon.com']:
        test(url,driver)