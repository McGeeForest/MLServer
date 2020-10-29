#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2019-12-07 21:27
"""
import os
import sys, logging
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from worker.yuqing.crawler.weibospider.spiders.tweet import TweetSpider
logger = logging.getLogger("")
logger.setLevel(logging.ERROR)
def weiboStarter(key_words):
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerRunner(settings)
    TweetSpider.key_words = key_words
    d = process.crawl(TweetSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()       # the script will block here until the crawling is finished
if __name__ == '__main__':
    mode = 'tweet'
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'tweet': TweetSpider
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
