# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

# change cookie to yours
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'SCF=AsZKV0CKeJKB_O0cntUmnwgo5BSu8sJg_QH4ulwbKpCqWdHxSNC6JQSYCVDYRKCp0yxrr-txFeVdEIfJ_1g_mZ4.; SUB=_2A25yR75eDeRhGeFK4lcU9CjJyjmIHXVRy8IWrDV6PUJbktANLWLYkW1NQqlLpSoTfGI_4mhY0oD_HvBLXYEqrgcV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhiXvxKyMmL8ikoME1hQKPb5JpX5KzhUgL.FoMX1K-fShqfeK-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMReKM0eKqp1h.E; SUHB=0d4OJ_bV_fZ9Kl; _WEIBO_UID=7495546515; _T_WM=a5bc4d6738a3c2941593ad7a079958b1'
}

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.MongoDBPipeline': 300,
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

# log相关
LOG_LEVEL = 'ERROR'
# LOG_FILE = 'log.txt'