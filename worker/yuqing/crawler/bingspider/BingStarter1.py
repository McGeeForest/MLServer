# -*- coding:utf-8 -*-
'''
从百度把前10页的搜索到的url爬取保存
'''

import time
from bs4 import BeautifulSoup  # 处理抓到的页面
import sys
import requests, requests_html
from requests_html  import HTMLSession,HTML
import importlib

importlib.reload(sys)  # 编码转换，python3默认utf-8,一般不用加
import urllib

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}  # 定义头文件，伪装成浏览器


def getfromBing(word):
    start = time.clock()
    url = 'https://cn.bing.com/search?q=' + urllib.parse.quote(word) + '%20site%3Anews.163.com&first=11'
    pages_num = 5           # 爬取前pages_num页
    curr_count = 0          # 控制递归爬取页面
    link_pair_list = []     # 存放捕获的链接
    geturl(url, curr_count, pages_num, link_pair_list)
    for i in link_pair_list:
        print(i[0])


def geturl(url, curr_count, pages_num, link_pair_list):
    curr_count += 1
    print("geturl", url)
    # response = requests.get(url=url, headers=headers, allow_redirects=False)
    session = HTMLSession()
    response = session.get(url=url)
    html = HTML(html=response.text)
    print(html.render())
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.select('#b_results > li.b_pag > nav > ul > li')[-1].find('a').get('href'))
    tagh2 = soup.find_all('h2')
    print(soup.select('#b_results > li.b_pag > nav > ul > li > a.sb_pagN')[0].get('href'))
    # print(soup.select('#b_results > li.b_pag > nav > ul > li'))
    url = 'https://cn.bing.com' + soup.select('#b_results > li.b_pag > nav > ul > li > a.sb_pagN')[0].get('href')
    print('下一页： ' + url)
    # print("=====")
    for h2 in tagh2:
        try:
            href = h2.find('a').get('href')
        except AttributeError:
            break
        title = h2.find('a').text
        if href.startswith('http'):
            link_pair_list.append((title, href))
    if curr_count == pages_num:
        return link_pair_list
    else:
        geturl(url, curr_count, pages_num, link_pair_list)


if __name__ == '__main__':
    getfromBing('泄露 爆炸')