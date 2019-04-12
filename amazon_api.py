import multiprocessing
import random
import time
import traceback
import sys
import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait       #WebDriverWait注意大小写
from selenium.webdriver.common.by import By
from setting import *
from selenium.common.exceptions import TimeoutException
import pymysql
import redis
import random as R
from setting import *
user_agent = [
           "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
           "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
           "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
       ]


headers= {
# ':authority': 'www.amazon.com',
# ':method': 'GET',
# ':path': '/dp/B07886XTCF',
# ':scheme': 'https',
# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
# 'cache-control':' max-age=0',
'cookie': 'session-id=140-8589342-6040104; ubid-main=130-0280656-3576606; x-wl-uid=1oDoosuuQ/eX4m9g2DiEGl8nFxyrgRna38RwY4XfGWis3AycEZIauY2XERPVVvCg4QYzo+9gDCvA=; i18n-prefs=USD; session-id-time=2082787201l; session-token=v9oMVKaomSS+3piRiotARu0uO6/htBEAdgt9j0DZhQcEdkpvOm5NPq3u6A7WhnZiUhGo6duKrwBy1kCZrPJlE5Ihu3DS0LXsFBsQ7yibURdA8Yk5l7WaLzhBmLVQ4z6meYF0MFEw7jX505X4g7ec9elEd0EwS8csYqR1XojgWANNsmmLbI3XMAtPcL+xltvJ; x-amz-captcha-1=1553514034204820; x-amz-captcha-2=boZbJQGor5U1XTb01KdimQ==; csm-hit=tb:BF6CMHYP9J5T11P30V7J+s-BF6CMHYP9J5T11P30V7J|1553578500301&t:1553578500301&adb:adblk_no',
'upgrade-insecure-requests': '1',
'user-agent': R.choice(user_agent),
"Referer":R.choice(ref),
"Origin":"https://www.amazon.com",
"Content-Type":"text/plain;charset=UTF-8",
"Connection": 'close',
"accept":"*/*",
}

def cnn_db():
    db = pymysql.connect("*.*.*.*", 'root', '*', '*', charset='utf8')
    return db

def get_asin_list(watch_style):
    db=cnn_db()
    cur=db.cursor()
    sql='select asin from asin_table where type="%s" and status=0;'%watch_style
    # sql='select asin from t2 where type="%s" and price=0 and pf=0 and rank=0;'%watch_style
    num = cur.execute(sql)
    print(num)
    sum_data=cur.fetchall()
    db.close()
    return sum_data

def next_selenium(asin,driver):
    driver.get("https://www.amazon.com/dp/" + asin)
    time.sleep(3)
    html=driver.page_source
    return [html,driver]


def selenium_down_loader(asin):
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-javascript ')
        # option.add_argument('--user-data-dir="chrome_cahce"')
        # option.add_argument('--disk-cache-dir="chrome_cahce"')
        capa = DesiredCapabilities.CHROME
        # option.add_argument('--first run')
        capa["pageLoadStrategy"] = "none"
        # option.add_argument('--headless')
        option.add_argument("--disable-javascript")
        option.add_argument("--no-sandbox")
        # option.add_argument('')
        option.add_argument('--user-agent=%s' % R.choice(user_agent))
        driver = webdriver.Chrome(CHROME_PATH, options=option, desired_capabilities=capa)
        wait = WebDriverWait(driver, 12)
        # driver.delete_all_cookies()
        driver.get("https://www.amazon.com/dp/" + asin)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='imgTagWrapper'] | //div[@class='a-row a-text-center']")))
        html=driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('title')
        #print(tags[0].text)
        if tags[0].text == 'Page Not Found':
            return html

        if tags[0].text == 'Robot Check':
            print("waring !!!,be check as robot!")
            try:
                driver.quit()
            except Exception as e:
                pass
            for i in range(10):
                print('\r stop last %s second' % (10 - i), end='')
                time.sleep(1)
            selenium_down_loader(asin)
    except TimeoutException:
        selenium_down_loader(asin)
    # finally:
    #     try:
    #         driver.quit()
    #     except Exception as e:
    #         pass
    # time.sleep(1)
    return [html,driver]



# 轻型下载器 requests
def down_loader(asin):
    # r = redis.Redis()
    # data = r.get('ip').decode().split('\n')[:-1]
    #
    # my_ip = R.choice(data)
    # proxies={
    #     'http':"%s"%my_ip,
    #     'https':"%s"%my_ip
    # }
    try:
        requests.adapters.DEFAULT_RETRIES = 3
        s = requests.session()
        s.keep_alive = False 
        # req = s.get('https://www.amazon.com/dp/%s'%asin,headers=headers,proxies=proxies,timeout=20)
        req = s.get('https://www.amazon.com/dp/%s' % asin, headers=headers, timeout=20)

        req.encoding='utf-8'
        html=req.text


        soup=BeautifulSoup(html,'html.parser')
        tags=soup.find_all('title')
        #print(tags[0].text)
        if tags[0].text == 'Page Not Found':
            return html


        if tags[0].text=='Robot Check':
            print("waring !!!,be check as robot!")
            for i in range(10):
                print('\r stop last %s second'%(10-i),end='')
                time.sleep(1)
            down_loader(asin)
        if req.status_code!=200:
            down_loader(asin)
    except Exception as e:
        print("!!!!",e)
        ex_type, ex_val, ex_stack = sys.exc_info()
        print(ex_type)
        print(ex_val)
        for stack in traceback.extract_tb(ex_stack):
            print(stack)
        down_loader(asin)
    # with open('test.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    return html
def analysis(asin,my_type,driver):
    print(asin)
    status_list=[1,1]
    status = R.choice(status_list)
    if status==0:
        html=down_loader(asin)
    else:
        # html=selenium_down_loader(asin)
        html = next_selenium(asin,driver)[0]
    html_x = etree.HTML(html)
    try:
        price=html_x.xpath("//div[@class='a-section a-spacing-small a-spacing-top-small']/span/a/b/following-sibling::text()")[0].split(' ')[-1][1:]
        price=price.replace(",",'')
    except Exception as e:
        price=0



    try:
        price=float(price)
    except Exception as e:
        print(e)
        price=0 # B01ICSF77M　WARING IN THIS SKU


    try:
        pf=html_x.xpath("//span/a/i/span")[0].text.split(' ')[0]
    except Exception as e:
        pf=0
    # print('price',price,'\npinfen',pf)

    try:
        rank_msg=html_x.xpath("//b[text()='Amazon Best Sellers Rank:']/following-sibling::text()")

        h = ''
        for rank in rank_msg:
            h+=rank
        big_rank=h.replace(',','')
        # print(big_rank.split(' ')[1].split("#")[1])
        if 'Clothing Shoes & Jewelry ()' in big_rank:
            big_rank=big_rank.split(' ')[1].split("#")[1]
            status=0
        else:
            # big_rank = big_rank.split(' ')[1].split("#")[1]  # 大排名
            big_rank=0
            status = 1# 有大排名，但不是    Clothing Shoes & Jewelry () 的大排名

    except Exception as e:
        big_rank=0
        status = 2  #　无大排名
        # print(big_rank)
    try:
        price=price.replace(',',"")
    except:
        pass
    print("""
    type:%s
    asin:%s
    price:%s
    pinfen:%s
    rank:%s
    status:%s
    """%(my_type,asin,price,pf,big_rank,status))
    print("*"*50)

    msg=[my_type,asin,float(price),float(pf),int(big_rank),status,2]
    # for i in msg:
    #     print(type(i),i)
    about_mysql(msg)
    return [my_type,asin[0],price,pf,big_rank]

def mul_main():
    p = multiprocessing.Pool(2)
    asin_list = get_asin_list('women')
    for asin in asin_list:
        p.apply_async(analysis,args=(asin[0],'women'))
    print('start for amazon')
    p.close()
    p.join()
    print('!!!')
    print("line to mysql..")

def about_mysql(msg):
    sql = 'insert into t2 values(0,"%s","%s",%s,%s,%s,now(),%s,%s);'%(msg[0],msg[1],msg[2],msg[3],msg[4],msg[5],msg[6])
    # sql='update t2 set price="%s",pf="%s",rank="%s",rank_status="%s" where asin="%s" and type="%s";'%(msg[2],msg[3],msg[4],msg[5],msg[1],msg[0])
    db = cnn_db()
    cur = db.cursor()
    cur.execute(sql)
    try:
        db.commit()
        print("%s has writed down"%msg[1])
        update_sql='update asin_table set status=1 where asin="%s" and type="%s";'%(msg[1],msg[0])
        cur.execute(update_sql)
        db.commit()
        print("table asin_table has changed!")
    except Exception as e:
        print("failed!",e)
        with open('bug.txt','a',encoding='utf-8') as f:
            f.write(msg[1]+e)
    db.close()
#

asin_list=get_asin_list('boy')
driver=selenium_down_loader(asin_list[0][0])[1]
for asin in asin_list[1:]:

    # time.sleep(R.choice([4.5,3,5.5,7,4.5,2])-2)
    analysis(asin[0],'boy',driver)

# analysis('B07JGXSRR9','women')
#mul_main()
