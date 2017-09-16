# encoding=utf-8

import urllib
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')


indie_index_gotit =False
qiyou_index_gotit=False
qiyou_nomal_gotit=False
baqipk_index_gotit=False
baqipk_nomal_gotit=False
dunwan_gotit =False
dunwan_index_gotit =False
siq5q_nomal_gotit =False
siq5q_index_gotit =False

debug = False # 设置是否打印log

# 找到的连接地址
dunwan_link = ""

indie_link = ""

baqipk_link = ""

siq5q_link = ""



def log(message):
    if debug:
        print( message)

def load_page_html(url):
    log('Get a html page :'+ url)
    return urllib.urlopen(url).read()


def download_html_indie( name):
    global indie_index_gotit
    global indie_link
    url = "http://indiegame.tv"
    html_context = load_page_html(url)
    if html_context.find(name) > 0:
        log("find index page in indie")
        indie_index_gotit =True


    news_url = "http://indiegame.tv/news"
    news_html_context = load_page_html(news_url)
    soup = BeautifulSoup(news_html_context, "html.parser")
    for ul_mode in soup.findAll('ul',{'class', 'list-pt clearfix'}):
        for a_mode in ul_mode.findAll('a',{'class', 'txt-box'}):
            if a_mode is not None and a_mode.has_attr('href') and a_mode.has_attr('title'):
                link_href = a_mode.attrs['href']
                ratio =fuzz.ratio(a_mode.attrs['title'], name)
                if ratio >80:
                    log("link:"+url+link_href)
                    indie_link = url+link_href



def download_dunwan_page_html(url, name):
    global dunwan_gotit
    global dunwan_link
    if dunwan_gotit:
        return
    html_context = load_page_html(url)
    html_context = unicode(html_context, 'GBK').encode('UTF-8')
    soup = BeautifulSoup(html_context, "html.parser")
    article_mode = soup.find('div',{'class', 'news_article'})
    for li_mode in article_mode.findAll('li'):
        a_mode =li_mode.find('a')
        if a_mode is not None and a_mode.has_attr('href') and a_mode.has_attr('title'):
            title = a_mode.attrs['title']
            link_href = a_mode.attrs['href']
            ratio = fuzz.ratio(title, name)
            if ratio > 80:
                dunwan_gotit=True
                dunwan_link = link_href



def download_dunwan_page(frm=1, page_count=10, name=""):
    for x in range(frm, frm+page_count):
        url = "http://www.dunwan.com/news/xinwen/list_3_%d.html"%x
        if x ==1:
            url = "http://www.dunwan.com/news/xinwen/"
        download_dunwan_page_html(url, name)


def download_dunwan_page_index(name):
    global dunwan_index_gotit

    index_url = "http://www.dunwan.com"
    html_context = load_page_html(index_url)
    html_context = unicode(html_context, 'GBK').encode('UTF-8')
    if html_context.find(name) > 0:
        log("find index page in dunwan")
        dunwan_index_gotit = True


    link = download_dunwan_page(frm=1, page_count=30,name=name)


def download_html_87pk_nomal_context(url, name):
    global baqipk_nomal_gotit
    global baqipk_link
    if baqipk_nomal_gotit:
        return
    html_context = load_page_html(url)
    soup = BeautifulSoup(html_context, "html.parser")
    ul_mode= soup.find('ul',{'class','sub_list'})
    for li_mode in ul_mode.findAll('li'):
        a_mode = li_mode.find('a')
        strname= a_mode.string
        ratio = fuzz.ratio(strname, name)
        if ratio > 80:
            log(a_mode.attrs['href'])
            baqipk_nomal_gotit =True
            baqipk_link= a_mode.attrs['href']




def download_html_87pk(name):
    global baqipk_index_gotit
    index_url = "http://www.87pk.com"
    html_context = load_page_html(index_url)
    html_context = unicode(html_context, 'GBK').encode('UTF-8')
    if html_context.find(name) > 0:
        log("find index page in 87pk")
        baqipk_index_gotit = True

    for i in range(1,30):
        url_nomal="http://www.87pk.com/news/yxxw/index_%d.html"%i
        download_html_87pk_nomal_context(url_nomal, name)


def download_html_qiyou(name):
    global qiyou_nomal_gotit
    index_url = "http://www.qigame.cn"
    html_context = load_page_html(index_url)
    if html_context.find(name) > 0:
        log("find index page in qiyou")

    for x in range(2, 20):
        nomal_url = "http://www.qigame.cn/news/index_%d.html"%x
        if x == 1:
            nomal_url = "http://www.qigame.cn/news/index.html"
        if qiyou_nomal_gotit:
            return
        html_context_nomal = load_page_html(nomal_url)
        soup = BeautifulSoup(html_context_nomal, "html.parser")
        for div_mode in soup.findAll('div',{'class', 'list_main'}):
            for li_mode in div_mode.findAll('div',{'class','art2'}):
                p_mode = li_mode.find('p', {'class','tit'})
                a_mode = p_mode.find('a')
                if a_mode is not None and a_mode.has_attr('title'):
                    a_title = a_mode.attrs['title']
                    ratio =fuzz.ratio(a_title, name)
                    if ratio >80 :
                        log(index_url+a_mode.attrs['href'])
                        qiyou_nomal_gotit =True

def download_html_4q5q (name):
    global siq5q_nomal_gotit
    global siq5q_index_gotit
    global siq5q_link
    main_url = "http://www.4q5q.com"
    index_url = "http://www.4q5q.com/news/index.html"
    html_context = load_page_html(index_url)
    if html_context.find(name) > 0:
        log("find index page in 4q5q")
        siq5q_index_gotit =True


    for x in range(1,30):
        if siq5q_nomal_gotit:
            return
        nomal_url ="http://www.4q5q.com/news/index.html?page=%d"%x
        html_context = load_page_html(nomal_url)
        soup = BeautifulSoup(html_context,"html.parser")
        for div_mode in soup.findAll('div',{'class','newstop'}):
             h2_mode = div_mode.find('h2')
             a_mode = h2_mode.find('a')
             if a_mode is not None and a_mode.has_attr('title'):
                 a_title = a_mode.attrs['title']
                 ratio =fuzz.ratio(a_title, name)
                 if ratio >80 :
                     log(main_url+a_mode.attrs['href'])
                     siq5q_link = main_url+a_mode.attrs['href']
                     siq5q_nomal_gotit =True


uxiyi_link = ""
uxiyi_index_gotit = False
uxiyi_nomal_gotit = False
def download_html_uxiyi (name):
    global uxiyi_index_gotit
    global uxiyi_link
    global uxiyi_nomal_gotit
    main_url = "http://www.uxiyi.com"
    html_context = load_page_html(main_url)
    index_name = name[0:5]
    if html_context.find(index_name) > 0:
        log("find index page in uxiyi")
        uxiyi_index_gotit = True

    for x in range(1,30):
        if uxiyi_nomal_gotit:
            return
        nomal_url = "http://www.uxiyi.com/news/shoujiwangyou/list_%d.html"%x
        html_context = load_page_html(nomal_url)
        soup = BeautifulSoup(html_context,"html.parser")
        for div_mode in soup.findAll('div',{'class','bd'}):
             ul_mode = div_mode.find('ul')
             if ul_mode is not None:
                 for li_mode in ul_mode.findAll('li'):
                     h3_mode = li_mode.find('h3')
                     if h3_mode is not None:
                         a_mode = h3_mode.find('a')
                         if a_mode is not None and a_mode.has_attr('href'):
                             a_title = a_mode.string
                             ratio =fuzz.ratio(a_title, name)
                             if ratio >80 :
                                 log(a_mode.attrs['href'])
                                 uxiyi_link = a_mode.attrs['href']
                                 uxiyi_nomal_gotit =True

zhuimeng_link = ""
zhuimeng_index_gotit = False
zhuimeng_nomal_gotit = False
def dowload_html_zhuimeng(name):
    global zhuimeng_link
    global zhuimeng_index_gotit
    global zhuimeng_nomal_gotit
    main_url = "http://www.dreamerd.com"
    html_context = load_page_html(main_url)
    index_name = name[0:5]
    if html_context.find(index_name) > 0:
        log("find index page in zhimemng")
        zhuimeng_index_gotit = True

    for x in range(1,30):
        if zhuimeng_nomal_gotit:
            return
        nomal_url = "http://www.dreamerd.com/zixun/index_%d.html"%x
        html_context = load_page_html(nomal_url)
        soup = BeautifulSoup(html_context,"html.parser")
        for div_mode in soup.findAll('div',{'class','list_main'}):
             ul_mode = div_mode.find('ul')
             if ul_mode is not None:
                 for li_mode in ul_mode.findAll('li'):
                     p_mode = li_mode.find('p',{'class','tit'})
                     if p_mode is not None:
                         a_mode = p_mode.find('a')
                         if a_mode is not None and a_mode.has_attr('href'):
                             a_title = a_mode.string
                             ratio =fuzz.ratio(a_title, name)
                             if ratio >80 :
                                 log(main_url+a_mode.attrs['href'])
                                 zhuimeng_link = main_url+a_mode.attrs['href']
                                 zhuimeng_nomal_gotit =True



sandm_link = ""
sandm_index_gotit =False
sandm_nomal_gotit = False
def download_html_3dm(name):
    global sandm_link
    global sandm_index_gotit
    global sandm_nomal_gotit
    main_url = "http://shouyou.3dmgame.com"
    html_context = load_page_html(main_url)
    index_name = name[0:6]
    if html_context.find(index_name) > 0:
        log("find index page in sandm")
        sandm_index_gotit =True

    for x in range(1,30):
        if sandm_nomal_gotit:
            return
        nomal_url = "http://shouyou.3dmgame.com/news/10_%d.html"%x
        html_context = load_page_html(nomal_url)
        soup = BeautifulSoup(html_context,"html.parser")
        for div_mode in soup.findAll('div',{'class','news-list'}):
             ul_mode = div_mode.find('ul')
             if ul_mode is not None:
                 for li_mode in ul_mode.findAll('li'):
                     if li_mode is not None:
                         a_mode = li_mode.find('a')
                         if a_mode is not None and a_mode.has_attr('href'):
                             a_title = a_mode.attrs['title']
                             ratio =fuzz.ratio(a_title, name)
                             if ratio >80 :
                                 log(main_url+a_mode.attrs['href'])
                                 sandm_link = main_url+a_mode.attrs['href']
                                 sandm_nomal_gotit =True


def getMyContext(site, index_gotit, link):
    index_position = "首页"
    nomal_position = "普文"
    if index_gotit:
        site_position = index_position
    else:
        site_position = nomal_position
    msg = site +"&nbsp&nbsp&nbsp&nbsp" +site_position+"&nbsp&nbsp&nbsp&nbsp" + link
    return msg



def main(name):
    global indie_link
    global dunwan_link

    download_html_indie( name)

    download_dunwan_page_index(name)

    download_html_87pk(name)

    download_html_qiyou(name)

    download_html_4q5q(name)

    download_html_uxiyi(name)

    dowload_html_zhuimeng(name)

    download_html_3dm(name)


    dunwan = "蹲玩"
    dunwan = getMyContext(dunwan, dunwan_index_gotit, dunwan_link)

    indie = "Indiegame"
    indie = getMyContext(indie, indie_index_gotit, indie_link)

    baqipk = "87pk"
    baqipk = getMyContext(baqipk, baqipk_index_gotit, baqipk_link)

    siq5q= "4q5q"
    siq5q = getMyContext(siq5q, siq5q_index_gotit, siq5q_link)

    uxiyi = "有蜥蜴"
    uxiyi = getMyContext (uxiyi, uxiyi_index_gotit, uxiyi_link)

    zhuimeng= "追梦网"
    zhuimeng = getMyContext(zhuimeng, zhuimeng_index_gotit, zhuimeng_link)

    sandm = "3DM"
    sandm = getMyContext(sandm, sandm_index_gotit , sandm_link)
    #
    return dunwan + "<br>" + indie +"<br>"+baqipk + "<br>" +siq5q + "<br>" + uxiyi +"<br>" +zhuimeng +"<br>" +sandm





# if __name__ == '__main__':
#     main()
