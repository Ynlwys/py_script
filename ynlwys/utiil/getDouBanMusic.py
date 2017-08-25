# -*- coding:utf-8 -*-


"""
    author：YNlwys


"""

import requests
import re
from bs4 import BeautifulSoup
import time
import pymongo
client = pymongo.MongoClient('localhost', 27017)
douban = client['douban']
musictop = douban['musictop']
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
def get_url_music(url):
    wb_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    music_hrefs = soup.select('a.nbg')
    for music_href in music_hrefs:
        get_music_info(music_href['href'])
        time.sleep(2)
def get_music_info(url):
    wb_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    names = soup.select('h1 > span')
    authors = soup.select('span.pl > a')
    styles = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />',wb_data.text,re.S)
    times = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />',wb_data.text,re.S)
    contents = soup.select('span.short > span')
    if len(names) == 0:
        name = '缺失'
    else:
        name = names[0].get_text()
    if len(authors) == 0:
        author = '佚名'
    else:
        author = authors[0].get_text()
    if len(styles) == 0:
        style = '未知'
    else:
        style = styles[0].split('\n')[0]
    if len(times) == 0:
        time = '未知'
    else:
        time = times[0].split('-')[0]
    if len(contents) == 0:
        content = '无'
    else:
        content = contents[0].get_text()
    info = {
        'name':name,
        'author':author,
        'style':style,
        'time':time,
        'content':content
    }
    musictop.insert_one(info)
for url in urls:
    get_url_music(url)
