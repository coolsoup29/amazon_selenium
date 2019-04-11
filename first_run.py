import pymysql
from selenium import webdriver
from urllib.parse import unquote
from bs4 import BeautifulSoup
from setting import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait       #WebDriverWait注意大小写
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


page=1
MAX_PAGE=500
def db_cnn():
    db=pymysql.connect(host,user,pwd,DDB,charset='utf8')
    return db

def insert_sql(msg):
    db=db_cnn()
    cur=db.cursor()
    try:
        cur.execute("insert into asin_table values(0,'%s','%s',now(),'%s',0);"%(msg[0],msg[1],msg[2]))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        db.close()

def get_asin_add_cookies(driver,f_type):
    global page
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"
    # driver=webdriver.Chrome(CHROME_PATH)
    # wait = WebDriverWait(driver, 20)

    # driver.get(asurl)


    # driver.set_page_load_timeout(5)
    # driver.set_script_timeout(5)  # 这两种设置都进行才有效
    # try:
    #     driver.get(asurl)
    # except:
    #     driver.execute_script('window.stop()')



    # wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='a-last']")))  # 这里可选择多个selector
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("div", 'a-section aok-relative s-image-square-aspect')
    for tag in tags:
        url = unquote(tag.parent.attrs['href'])
        asin = url.split("/dp/")[1].split('/')[0]
        try:
            print(asin, tag.contents[1].attrs['src'])
            insert_sql([asin, tag.contents[1].attrs['src'],f_type])
        except Exception as e:
            continue
    # driver.get('https://www.amazon.com/s?k=watches&rh=n%3A7147441011%2Cn%3A6358540011&dc&qid=1553074545&rnid=2941120011&ref=sr_nr_n_2')

    try:
        # next_url='https://www.amazon.com'+soup.find_all('li','a-last')[0].contents[0].attrs['href']
        driver.find_elements_by_xpath("//li[@class='a-last']")[0].click()
    except:
        get_asin_add_cookies(driver,f_type)
    # driver.quit()
    page+=1
    print("had done %s page" % page)
    # print(next_url)
    if page <MAX_PAGE:
        get_asin_add_cookies(driver,f_type)
    else:
        print("all done！")

def get_asin(asurl,f_type):
    global page
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver=webdriver.Chrome(CHROME_PATH,desired_capabilities=capa,options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    driver.get(asurl)

    wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='a-last']")))  # 这里可选择多个selector
    html = driver.page_source
    driver.save_screenshot('p1.png')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("div", 'a-section aok-relative s-image-square-aspect')
    for tag in tags:
        url = unquote(tag.parent.attrs['href'])
        asin = url.split("/dp/")[1].split('/')[0]
        print(asin, tag.contents[1].attrs['src'])
        insert_sql([asin,tag.contents[1].attrs['src'],f_type])

    print("had done %s page"%page)
    # next_url='https://www.amazon.com'+soup.find_all('li','a-last')[0].contents[0].attrs['href']
    # print(next_url)
    driver.find_elements_by_xpath("//li[@class='a-last']")[0].click()
    get_asin_add_cookies(driver,f_type)






# get_asin('https://www.amazon.com/s?k=watches&rh=n%3A7147441011%2Cn%3A6358540011&dc&qid=1553074545&rnid=2941120011&ref=sr_nr_n_2')
get_asin('https://www.amazon.com/s?k=watches&rh=n%3A7147440011%2Cn%3A6358544011&dc&qid=1554980068&rnid=2941120011&ref=sr_nr_n_6','women')










