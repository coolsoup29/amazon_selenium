import requests
from bs4 import BeautifulSoup
import pymysql
from setting import *
from lxml import etree

def cnn_db():
    db=pymysql.connect("localhost",'root','yice1821','test')
    return db


def down_loader(url):
    headers = {
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
        "Referer": R.choice(ref),
        "Origin": "https://www.amazon.com",
        "Content-Type": "text/plain;charset=UTF-8",
        "Connection": 'close',
        "accept": "*/*",
    }

    requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    # req = s.get('https://www.amazon.com/dp/%s'%asin,headers=headers,proxies=proxies,timeout=20)
    req = s.get(url, headers=headers, timeout=20)

    req.encoding = 'utf-8'
    html = req.text
    return html

def insert(msg):
    create_table_sql='create table WORD_SPSS(id int primary key auto_increment,type varchar(10),word varchar(30) not null,freq int default 0,site varchar(20) not null,time date)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'
    limit_sql = 'alter table WORD_SPSS add constraint lim_word_time unique(word,time,type);'
    db=cnn_db()
    cur=db.cursor()
    insert_sql='insert into WORD_SPSS values(0,"%s","%s",%s,"%s",now());'%(msg[0],msg[1],msg[2],msg[3])
    try:
        print(insert_sql)
        cur.execute(insert_sql)
        db.commit()
        print("%s写入完成"%msg[1])
    except Exception as e:
        print(e,"写入失败!",msg)

def it_analysis(url):
    pass


def main(site,url,type):
    ALL_TITLE = ''
    print(url)
    html=down_loader(url)
    html_x = etree.HTML(html)

    title_list=html_x.xpath('//div[@class="a-section a-spacing-small"]/../../span/following-sibling::div[text()]')
    for title in title_list:
        print(title.text.split("\n")[1].strip())
        ALL_TITLE+=' '+title.text.split("\n")[1].strip()

    next_page=html_x.xpath("//li[@class='a-last']/a/@href")[0]
    print("next_page",next_page)
    html = down_loader(next_page)
    html_x = etree.HTML(html)

    title_list = html_x.xpath('//div[@class="a-section a-spacing-small"]/../../span/following-sibling::div[text()]')
    for title in title_list:
        print(title.text.split("\n")[1].strip())
        ALL_TITLE += ' ' + title.text.split("\n")[1].strip()

    word_list=ALL_TITLE.replace(',',' ').replace(':',' ').split(" ")
    set_word = list(set(word_list))
    try:
        set_word= set_word.remove(":")
    except:
        pass
    try:
        set_word=set_word.remove("-:")
    except:
        pass
    for word in set_word:
        sum_word=0
        for each_word in word_list:
            if word==each_word:
                sum_word+=1
        print(word,sum_word)
        msg=[type,word,sum_word,site]
        insert(msg)
if __name__ == '__main__':
    # sex_type='girl'
    for site in ['UK','DE','US','ES','CA','FR','IT']:  #'UK','DE','US','IT',,'ES','CA','FR','JP'
        for sex_type in ['men','women','girl','boy']:
            main(site,locals()[site][sex_type],sex_type)
