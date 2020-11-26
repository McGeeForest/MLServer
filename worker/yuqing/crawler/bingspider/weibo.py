import time
import urllib
from urllib import request
from urllib.parse import quote
import string
from lxml import etree
from worker.yuqing.crawler.bingspider.utils import *

headers={
    'cookie': 'SCF=AsgKsGlIYOASs6D1liNbIvr-IJmdywutRR0TeMd3FONPxJ00N98zO-LWjbj0N_VIPcRQETULxPTsWDQUhMp9k6c.; SUB=_2A25yfvHxDeRhGeNN61sR9i7EwjuIHXVRgJ-5rDV6PUJbktAKLW_ekW1NSU_KkFOOHCZfCDyNf6ua8AfqSAtr1QhW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWjQZI50Arb0eqJ-dsNqj7z5JpX5K-hUgL.Fo-0eh.7So5R1KM2dJLoIXnLxKqL1-eL1h.LxK.LB-BL1KBLxKqLBoeL1K-LxKML1-2L1hBLxKnLB.qLBoMLxK.L1-zLB.-LxKqLBKeLB--LxKqL1--L1KMt; SUHB=0G0u7g0-7wOaPH; SSOLoginState=1601864097; _T_WM=23360542304',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

keywords = ['火灾']
# keywords = self.key_words
date_end = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')  # 当前时间
date_start = date_end - datetime.timedelta(days=10)  # 开始是前10天
time_spread = datetime.timedelta(days=1)
urls = []
url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
while date_start < date_end:
    next_time = date_start + time_spread * 2  # 一天一天的爬取
    urls.extend(
        [url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
         for keyword in keywords]
    )
    date_start = next_time
    # print("看这里"+str(urls))

print(urls)

for url in urls:
    s = quote(url, safe=string.printable)
    url = urllib.parse.quote(url, safe=string.printable)
    request = urllib.request.Request(url=url, headers=headers, method='GET')
    response = urllib.request.urlopen(request, timeout=5)
    print(response.read().decode("UTF-8"))
    print(response.url)




    if response.url.endswith('page=1'):
        all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
        if all_page:
            all_page = all_page.group(1)
            all_page = int(all_page)
            for page_num in range(2, all_page + 1):
                page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                print(page_url)
                break
                yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
    tree_node = etree.HTML(response.body)
    tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
    for tweet_node in tweet_nodes:
        try:
            tweet_item = {}
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

                tweet_item['news_timeStamp'] = int(
                    time.mktime(time.strptime(str(time_fix(create_time_info.split('来自')[0].strip())), "%Y-%m-%d %H:%M")))
                # tweet_item['tool'] = create_time_info.split('来自')[1].strip()
            else:
                tweet_item['news_timeStamp'] = int(
                    time.mktime(time.strptime(str(time_fix(create_time_info.strip())), "%Y-%m-%d %H:%M")))

            # like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            # tweet_item['like_num'] = int(re.search('\d+', like_num).group())

            # repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
            # tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())

            # comment_num = tweet_node.xpath(
            #     './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
            # tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())

            # print(tweet_node.xpath('//a[@class="cc"]')[-1].get('href'))
            comment_link = [tweet_node.xpath('.//a[@class="cc"]')[i].get('href') for i in
                            range(len(tweet_node.xpath('.//a[@class="cc"]')))][-1]
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