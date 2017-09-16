# encoding=utf-8

import urllib
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')


qiyou_index_gotit=False
qiyou_nomal_gotit=False
baqipk_index_gotit=False
baqipk_nomal_gotit=False
dunwan_gotit =False
debug = True # 设置是否打印log

def log(message):
    if debug:
        print( message)

def load_page_html(url):
    log('Get a html page :'+ url)
    return urllib.urlopen(url).read()


def download_html_indie( name):
    url = "http://indiegame.tv"
    html_context = load_page_html(url)
    soup = BeautifulSoup(html_context, "html.parser")
    for ul_mode in soup.findAll('ul',{'class', 'center_list'}):
        for a_mode in ul_mode.findAll('a'):
            if a_mode is not None and a_mode.has_attr('href'):
                link_href = a_mode.attrs['href']
                ratio =fuzz.ratio(a_mode.string, name)
                if ratio >90:
                    log("link:"+url+link_href)

def download_dunwan_page_html(url, name):
    global dunwan_gotit
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
                log("dunwan"+link_href)
                dunwan_gotit=True



def download_dunwan_page(frm=1, page_count=1, name=""):
    for x in range(frm, frm+page_count):
        url = "http://www.dunwan.com/news/xinwen/list_3_%d.html"%x
        download_dunwan_page_html(url, name)

def download_dunwan_page_index(name):
    url = "http://www.dunwan.com"
    html_context = load_page_html(url)
    html_context = unicode(html_context, 'GBK').encode('UTF-8')
    if html_context.find(name) > 0:
        log("find dunwan in index")



def download_html_87pk_nomal_context(url, name):
    global baqipk_index_gotit
    global baqipk_nomal_gotit
    if baqipk_index_gotit:
        return
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



def download_html_87pk(name):
    index_url = "http://www.87pk.com"
    html_context = load_page_html(index_url)
    html_context = unicode(html_context, 'GBK').encode('UTF-8')
    if html_context.find(name) > 0:
        log("find index page in 87pk")
        return

    for i in range(1,30):
        url_nomal="http://www.87pk.com/news/yxxw/index_%d.html"%i
        download_html_87pk_nomal_context(url_nomal, name)

def download_html_qiyou(name):
    global qiyou_nomal_gotit
    index_url = "http://www.qigame.cn"
    html_context = load_page_html(index_url)
    if html_context.find(name) > 0:
        log("find index page in qiyou")
        return

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


def main():
    name = "《剑与家园》主题曲悬念曝光 邓紫棋张韶涵陈一发儿傻傻分不清楚"


    download_html_indie( name)

    download_dunwan_page(frm=1, page_count=30,name=name)

    download_dunwan_page_index(name)

    download_html_87pk(name)

    download_html_qiyou(name)



if __name__ == '__main__':
    main()
