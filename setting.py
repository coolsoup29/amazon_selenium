import csv
import re
import time
from urllib.parse import unquote
import xlsxwriter
from PIL import Image
import random as R

MAIN_WORD='men watches'


CHROME_PATH='/home/yice/Desktop/set_driver/chromedriver'
# the href of sku
REQUEST_FILE = './cache/dp_women'
# the msg of sku
RESPONSE_FILE = 'newTEST_women0315'
#process count
PROCESS_COUNT=16
# the max time of loading
LOAD_TIME=20
# the max open for one href
MAX_TRY = 4
# the num of open
START_TRY=0


# user-agent
user_agent = [
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

# the site of search
ref = ["http://www.yahoo.com",
        "http://www.yandex.ru",
        "http://www.bing.com",
        "http://www.google.com.hk",
        "http://www.naver.com",
        "http://www.rambler.ru",
        "http://www.goo.ne.jp",
        "http://www.go.com",
        "http://www.webcrawler.com",
        "http://www.tiscali.it",
        "http://www.excite.com",
        "http://www.meta.ua",
        "http://www.search.com",
        "http://saucenao.com",
        "http://www.cari.com.my",
        "http://www.looksmart.com",
        "http://www.lycos.com",
        "http://infospace.com",
        "http://www.wlw.de",
        "http://www.najdi.si",
        "http://www.ciao.es",
        "http://www.dmoz.org",
        "http://www.ceek.jp",
        "http://www.fireball.de",
        "http://www.jubii.dk",
        "http://www.hotbot.com",
        "http://www.sputtr.com",
        "http://www.splut.com",
        "http://www.hit-parade.com",
        "http://www.goto.com",
        "http://www.voila.fr",
        "http://www.altavista.com",
        "http://www.accoona.com",
        "http://www.all.by",
        "http://www.gogreece.com",
        "http://www.bellnet.de",
        "http://www.searchengine.com",
        "http://www.slider.com",
        "http://www.newmalaysia.com",
        "http://www.abrexa.co.uk",
        "http://www.kellysearch.com",
        "http://www.anzwers.com.au",
        "http://torrent-finder.info",
        "http://www.sunsteam.com",
        "http://www.blinde-kuh.ch",
        "http://www.godado.it",
        "http://www.apali.com",
        "http://www.buscapique.com",
        "http://www.walhello.com",
        "http://infoo.se",
        "http://www.akavita.by",
        "http://www.acoon.de",
        "http://www.helles-koepfchen.ch",
        "http://www.google.com",
        "http://www.yippy.com",
        "http://www.abacho.ch",
        "http://www.cnous.ch",
        "http://www.abacho.com",
        "http://www.cusco.pt",
        "http://www.yabba.com",
        ]



headers_img = {
                    # "Host":"https://www.amazon.com",
                    "User-Agent": R.choice(user_agent),
                    "Referer":R.choice(ref),
                    # "cookie":'session-id=145-3838204-7005756; session-id-time=2082787201l; x-wl-uid=1J//Z2wsp58tRr8LvftT1v49sbAOV+ChJT+fhuzG9rpY9B1AI674VCAjLoz1BTQFs0PKH0yyZfT8=; ubid-main=131-7182398-2813924; session-token="GuP0WQPzQSyQ0QghypX/7Qj0hdjsyqT6vstdgTU2YzMor71/1G4d7dDd1uWwJ9l3PNtLZ8uaRV6kuqlzaDXMc1n+UioYNEg1TJdqzXzDoOLuwdhPZSu+ylxwr8YAdgap23n10zR/+qEpcEuqUkqdWUlqIy6mzfP0libqWtQDAxamE+51pcOBgnjw7L5osmqv/qXLUUFnMm7HTWt97PJHyEgIs8rvkFO/sQsusBYRAElWfZUeT+0MvNVOEesl2IqYDjmwro9rAz0="; i18n-prefs=USD; skin=noskin; csm-hit=tb:s-BN5GCF5KH7RKDSYA6KB8|1551723335320&t:1551723339458&adb:adblk_no',
                    "Origin":"https://www.amazon.com",
                    "Content-Type":"text/plain;charset=UTF-8",
                    "Connection": 'close',
                    "accept":"*/*",
                    }


US={
        'men':'https://www.amazon.com/gp/bestsellers/fashion/6358540011/ref=pd_zg_hrsr_fashion_2_1_last',
        'women':'https://www.amazon.com/gp/bestsellers/fashion/6358544011/ref=pd_zg_hrsr_fashion_1_1_last',
        'boy':'https://www.amazon.com/gp/bestsellers/fashion/6358552011/ref=pd_zg_hrsr_fashion_2_1_last',
        'girl':'https://www.amazon.com/gp/bestsellers/fashion/6358548011/ref=pd_zg_hrsr_fashion_1_1_last'
}



# fr
FR={
        'men':'https://www.amazon.fr/gp/bestsellers/watch/10143456031/ref=zg_bs_nav_watch_1_watch',
        'women':'https://www.amazon.fr/gp/bestsellers/watch/10143466031/ref=zg_bs_nav_watch_1_watch',
        'boy':'https://www.amazon.fr/gp/bestsellers/watch/10143448031/ref=zg_bs_nav_watch_1_watch',
        'girl':'https://www.amazon.fr/gp/bestsellers/watch/10143452031/ref=zg_bs_nav_watch_1_watch'
}



#de
DE={
        'men':'https://www.amazon.de/gp/bestsellers/watch/10084739031/ref=zg_bs_nav_watches_1_watches',
        'women':'https://www.amazon.de/gp/bestsellers/watch/10084749031/ref=zg_bs_nav_watches_1_watches',
        'boy':'https://www.amazon.de/gp/bestsellers/watch/10084731031/ref=zg_bs_nav_watches_1_watches',
        'girl':'https://www.amazon.de/gp/bestsellers/watch/10084735031/ref=zg_bs_nav_watches_1_watches',
}


UK={
        'men':'https://www.amazon.co.uk/Best-Sellers-Watches-Mens/zgbs/watch/10103528031/ref=zg_bs_nav_watches_1_watches',
        'women':"https://www.amazon.co.uk/Best-Sellers-Watches-Womens/zgbs/watch/10103527031/ref=zg_bs_nav_watches_1_watches",
        'boy':'https://www.amazon.co.uk/Best-Sellers-Watches-Boys/zgbs/watch/10103530031/ref=zg_bs_nav_watches_1_watches',
        'girl':'https://www.amazon.co.uk/Best-Sellers-Watches-Girls/zgbs/watch/10103529031/ref=zg_bs_nav_watches_1_watches'

}

IT={
        'men':'https://www.amazon.it/gp/bestsellers/watch/10112458031/ref=zg_bs_nav_w_1_w',
        'women':'https://www.amazon.it/gp/bestsellers/watch/10112454031/ref=zg_bs_nav_w_1_w',
        'boy':'https://www.amazon.it/gp/bestsellers/watch/10112466031/ref=zg_bs_nav_w_1_w',
        'girl':'https://www.amazon.it/gp/bestsellers/watch/10112462031/ref=zg_bs_nav_w_1_w'
}

ES={
        'men':'https://www.amazon.es/gp/bestsellers/watch/10117368031/ref=zg_bs_nav_w_1_w',
        'women':'https://www.amazon.es/gp/bestsellers/watch/10117375031/ref=zg_bs_nav_w_1_w',
        'boy':'https://www.amazon.es/gp/bestsellers/watch/10117360031/ref=zg_bs_nav_w_1_w',
        'girl':'https://www.amazon.es/gp/bestsellers/watch/10117364031/ref=zg_bs_nav_w_1_w'
}

CA={
        'men':'https://www.amazon.ca/Best-Sellers-Watches-Mens/zgbs/watch/7012516011/ref=zg_bs_nav_w_1_w',
        'women':'https://www.amazon.ca/Best-Sellers-Watches-Womens/zgbs/watch/7012520011/ref=zg_bs_nav_w_1_w',
        'boy':'https://www.amazon.ca/Best-Sellers-Watches-Boys/zgbs/watch/7012507011/ref=zg_bs_nav_w_1_w',
        'girl':'https://www.amazon.ca/Best-Sellers-Watches-Girls/zgbs/watch/7012511011/ref=zg_bs_nav_w_1_w'
}



# 日本站点区别　其他站点
# 每页 20 商品
# 一行一商品
JP={
        'men':"https://www.amazon.co.jp/gp/bestsellers/watch/333009011/ref=pd_zg_hrsr_watch_1_1_last",
        'women':'https://www.amazon.co.jp/gp/bestsellers/watch/333010011/ref=zg_bs_nav_w_2_333009011',
        'boy':'https://www.amazon.co.jp/gp/bestsellers/watch/2226425051/ref=zg_bs_nav_w_2_333009011',
        'girl':'https://www.amazon.co.jp/gp/bestsellers/watch/2226426051/ref=zg_bs_nav_w_2_333009011'
}

host="111.230.10.127"
user='root'
pwd='coolsoup'
DDB='test'



