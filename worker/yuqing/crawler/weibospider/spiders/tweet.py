#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import datetime,requests
import re
from lxml import etree
from bs4 import BeautifulSoup as bs
from scrapy import Spider
from scrapy.http import Request
import time
from worker.yuqing.crawler.weibospider.items import TweetItem
from worker.yuqing.crawler.weibospider.spiders.utils import time_fix, extract_weibo_content
from worker.yuqing.crawler.weibospider import settings

def getComments(page_url):
    page_url = page_url.split("#")[0] + '&page=1'
    # page_url = 'https://weibo.cn/comment/Je6J949RR?uid=7484746694&rl=1&page=1'
    curr_page = 1
    comment_items = []
    comment_response = requests.get(page_url, headers=settings.DEFAULT_REQUEST_HEADERS)
    # comment_response.encoding = comment_response.apparent_encoding  # 编码问题
    comment_response.encoding = 'UTF-8'  # 编码问题
    soup = bs(comment_response.text, 'lxml')
    # print(comment_response.text.find('还没有人针对这条微博发表评论!'))
    # print("回复按钮和赞按钮的数量:", len(soup.select('span.cc > a')))      # 是 0 的话，说明没有评论信息，返回空list
    if len(soup.select('span.cc > a')) == 0:
        # print("return []")
        return []
    else:
        # print('下一页按钮：', soup.select('#pagelist > form > div'))
        all_page = 0
        if len(soup.select('#pagelist > form > div'))!=0:
            p1 = re.compile(pattern='(?<=/).*?(?=页)', flags=re.IGNORECASE)       # 最小匹配，获得页数
            all_page = int(re.findall(p1, str(soup.select('#pagelist > form > div')[0].text))[0])
        # print('all page:', all_page)


        # 获取第一页内容
        item_id_list = []
        temp_item_id_list = soup.select('div')
        for item_id in temp_item_id_list:
            item_id = str(item_id)
            if item_id.startswith('<div class="c" id="C_'):
                p2 = re.compile(pattern='(?<=id="C_).*?(?=">)', flags=re.IGNORECASE)
                comment_id = re.findall(p2, item_id)[0]
                item_id_list.append(comment_id)

        temp_item_content_list = soup.select('div.c > span.ctt')
        item_content_list = [item.text for item in temp_item_content_list]
        temp_item_datetime_list = soup.select('div.c > span.ct')
        item_datetime_list = [str(datetime.datetime.now().year)+"年" + str(date_time.text).split("来自")[0].replace("\xa0","").replace(" ", "") for date_time in temp_item_datetime_list]

        temp_item_userid_list = soup.select('div.c > a')
        item_userid_list = []
        for i in range(len(temp_item_userid_list)):
            link = str(temp_item_userid_list[i].get('href'))
            if link.startswith('/u/'):
                item_userid_list.append(link.replace("/u/", ""))

        # print(page_url, all_page, len(item_content_list), len(item_datetime_list), len(item_userid_list))

        if all_page>1:
            for i in range(all_page-1):
                page_url = page_url.replace('page='+str(curr_page), 'page='+str(curr_page+1))
                curr_page += 1

                comment_response = requests.get(page_url, headers=settings.DEFAULT_REQUEST_HEADERS)
                # comment_response.encoding = comment_response.apparent_encoding  # 编码问题
                comment_response.encoding = 'UTF-8'  # 编码问题
                soup = bs(comment_response.text, 'lxml')
                # 获取第curr_page页内容
                temp_item_id_list = soup.select('div')
                for item_id in temp_item_id_list:
                    item_id = str(item_id)
                    if item_id.startswith('<div class="c" id="C_'):
                        p2 = re.compile(pattern='(?<=id="C_).*?(?=">)', flags=re.IGNORECASE)
                        comment_id = re.findall(p2, item_id)[0]
                        item_id_list.append(comment_id)

                temp_item_content_list = soup.select('div.c > span.ctt')
                item_content_list += [item.text for item in temp_item_content_list]
                temp_item_datetime_list = soup.select('div.c > span.ct')
                item_datetime_list += [
                    str(datetime.datetime.now().year) + "年" + str(date_time.text).split("来自")[0].replace("\xa0",
                                                                                                         "").replace(" ",
                                                                                                                     "")
                    for date_time in temp_item_datetime_list]

                temp_item_userid_list = soup.select('div.c > a')
                for i in range(len(temp_item_userid_list)):
                    link = str(temp_item_userid_list[i].get('href'))
                    if link.startswith('/u/'):
                        item_userid_list.append(link.replace("/u/", ""))
            # print(page_url, len(item_id_list), len(item_content_list), len(item_datetime_list), len(item_userid_list))
            # print(item_content_list)

            # len(item_id_list), len(item_content_list), len(item_datetime_list), len(item_userid_list)四个字段整合为一个评论
        for i in range(len(item_id_list)):
            comment_items.append({
                'comment_id': item_id_list[i],
                'comment_content': item_content_list[i],
                'comment_datetime': int(time.mktime(time.strptime(str(item_datetime_list[i]), "%Y年%m月%d日%H:%M"))),
                'comment_userid': item_userid_list[i]
            })
        # print(page_url)
        # print(comment_items)
        return comment_items

class TweetSpider(Spider):
    name = "tweet_spider"
    base_url = "https://weibo.cn"
    key_words = []

    def start_requests(self):

        def init_url_by_user_id():
            "crawl tweets post by users"
            user_ids = ['1087770692', '1699432410', '1266321801']
            urls = [f'{self.base_url}/{user_id}/profile?page=1' for user_id in user_ids]
            return urls

        def init_url_by_keywords():
            # crawl tweets include keywords in a period, you can change the following keywords and date
            # keywords = ['火灾']
            keywords = self.key_words
            date_end = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')       # 当前时间
            date_start = date_end - datetime.timedelta(days=10)                                  # 开始是前10天
            time_spread = datetime.timedelta(days=1)
            urls = []
            url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
            while date_start < date_end:
                next_time = date_start + time_spread*2        # 一天一天的爬取
                urls.extend(
                    [url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
                     for keyword in keywords]
                )
                date_start = next_time
                # print("看这里"+str(urls))

            return urls

        # select urls generation by the following code
        #urls = init_url_by_user_id()
        urls = init_url_by_keywords()
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetItem()
                # tweet_item['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['news_link'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),
                                                                           user_tweet_id.group(1))
                tweet_item['news_author'] = user_tweet_id.group(2)
                # tweet_item['_id'] = user_tweet_id.group(1)
                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:

                    tweet_item['news_timeStamp'] = int(time.mktime(time.strptime(str(time_fix(create_time_info.split('来自')[0].strip())), "%Y-%m-%d %H:%M")))
                    # tweet_item['tool'] = create_time_info.split('来自')[1].strip()
                else:
                    tweet_item['news_timeStamp'] = int(time.mktime(time.strptime(str(time_fix(create_time_info.strip())), "%Y-%m-%d %H:%M")))

                # like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                # tweet_item['like_num'] = int(re.search('\d+', like_num).group())

                # repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                # tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())

                # comment_num = tweet_node.xpath(
                #     './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                # tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())

                # print(tweet_node.xpath('//a[@class="cc"]')[-1].get('href'))
                comment_link = [tweet_node.xpath('.//a[@class="cc"]')[i].get('href') for i in range(len(tweet_node.xpath('.//a[@class="cc"]')))][-1]
                tweet_item['news_comments_link'] = comment_link
                tweet_item['news_comments'] = getComments(comment_link)
                tweet_item['news_site'] = 'www.weibo.com'

                # print("hjsbgdisbidfbsuidbfusdfbui", tweet_item)
                images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                if images:
                    tweet_item['image_url'] = images

                videos = tweet_node.xpath('.//a[contains(@href,"https://m.weibo.cn/s/video/show?object_id=")]/@href')
                if videos:
                    tweet_item['video_url'] = videos

                # map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                # if map_node:
                #     map_node = map_node[0]
                #     map_node_url = map_node.xpath('./@href')[0]
                #     map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                    # tweet_item['location_map_info'] = map_info

                repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                if repost_node:
                    tweet_item['origin_weibo'] = repost_node[0]

                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': tweet_item},
                                  priority=1)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    tweet_item['news_content'] = extract_weibo_content(tweet_html)


                    yield tweet_item

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html)
        yield tweet_item
