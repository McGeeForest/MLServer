# 目前使用

from selenium import webdriver
import urllib, requests, time, random, json
from bs4 import BeautifulSoup  # 处理抓到的页面
import worker.yuqing.crawler.bingspider.Site163Crawler as Site163Crawler
import worker.yuqing.crawler.bingspider.SiteQQCrawler as SiteQQCrawler
import worker.yuqing.crawler.bingspider.SiteThepaperCrawler as SiteThepaperCrawler

def starter(headers, key_word, page_count, listend_sites, url_dict):
    link_pair_list = []
    # 1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
    chromedriver = 'worker/yuqing/crawler/driver/chromedriver_win.exe'
    browser = webdriver.Chrome(chromedriver)
    def sub_pages(browser, headers, key_words, page_count, listend_site):
        link_pair_list = []
        # browser.get('https://cn.bing.com/')
        browser.get('https://global.bing.com/?FORM=HPCNEN&setlang=en-us&setmkt=en-us')
        # browser.find_element_by_css_selector('#est_en').click()
        time.sleep(random.random())
        browser.find_element_by_css_selector('#sb_form_q').send_keys(key_words)     # 输入要搜索的字符串
        time.sleep(random.random())
        # browser.find_element_by_css_selector('#sb_form > label').click()            # 点击搜索
        browser.find_element_by_css_selector('#sb_go_par').click()            # 点击搜索
        # 2.通过浏览器向服务器发送URL请求
        print(key_words)
        # url = 'https://cn.bing.com/search?q=' + urllib.parse.quote(key_words)     # word为关键词，pn是百度用来分页的
        # browser.get(url)
        time.sleep(random.random())
        # ele = browser.find_element_by_css_selector('span.fs_label')
        try_count = 0
        while try_count < 200:      # 无法选定时间则跳出
            time.sleep(0.1)
            try_count += 1
            try:
                browser.find_element_by_css_selector('span.fs_label').click()
                time.sleep(0.5)
                browser.find_element_by_css_selector('#ftrD_Any_time > a:nth-child(5)').click()
                print('点击成功跳出循环')
                break
            except:
                print("点击失败继续尝试")
                continue
        if try_count == 200:
            # print('设置搜索时间失败，返回空数据，切换下一组数据')
            # return []
            print('设置搜索时间失败，递归重启浏览器')
            return starter(headers, key_word, page_count, listend_sites, url_dict)


        time.sleep(random.random())
        # browser.find_element_by_css_selector().click()
        # print(url)
        curr_page = 0
        for page in range(page_count):
            curr_page += 1
            if curr_page > page_count:
                break

            browser.get(browser.current_url)
            html_page = browser.page_source
            soup = BeautifulSoup(html_page, 'lxml')
            tagh2 = soup.find_all('h2')

            for h2 in tagh2:
                browser.set_window_size(1000+curr_page, 800+curr_page)
                try:
                    href = h2.find('a').get('href')
                except AttributeError:
                    break
                tltle = h2.find('a').text
                # print(href)
                if href.startswith('http'):
                    link_pair_list.append([key_words, tltle, href.replace(" ",'')])
                # print("============")
            try:
                if curr_page == 1:
                    browser.find_element_by_css_selector('#bnp_hfly_cta2').click()
                    time.sleep(random.random())
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")    # 滑动到最底部
                time.sleep(random.random())
                browser.find_element_by_css_selector('#b_results > li.b_pag > nav > ul > li > a.sb_pagN').click()   # 切换下一页
                time.sleep(random.random())
            except:
                pass
        return link_pair_list

    for listend_site in listend_sites:
        # temp = ' '.join(key_words)
        search_string = key_word + ' site:' + listend_site
        sub_link_pair_list = sub_pages(browser, headers, search_string, page_count, listend_site)
        url_dict[listend_site].extend(sub_link_pair_list)
        # print(sub_link_pair_list)
        link_pair_list.append(sub_link_pair_list)
    return url_dict


# 供上层调用
def BingStarter(key_words):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }  # 定义头文件，伪装成浏览器

    listend_sites = ['news.163.com', 'news.qq.com', 'news.sohu.com', 'www.thepaper.cn']  # 写死无需更改
    # listend_sites = ['news.163.com', 'news.qq.com']  # 写死无需更改
    # 转存为四个网站的待爬取url，格式dict : {site1:[(keyword,(urltitle,url)), (keyword,url), (keyword,url)], site2:[(keyword,url), (keyword,url), (keyword,url)], site3:[(keyword,url), (keyword,url), (keyword,url)], site4:[(keyword,url), (keyword,url), (keyword,url)]}
    url_dict = {}
    for listend_site in listend_sites:
        url_dict[listend_site] = []
    for key_word in key_words:
        final_url_dict = starter(headers, key_word=key_word, page_count=1, listend_sites=listend_sites, url_dict=url_dict)
    url_json = json.dumps(url_dict, ensure_ascii=False)     # json格式
    news163 = url_dict['news.163.com']
    news163_dicts = Site163Crawler.site163starter(news163)
    newsqq = url_dict['news.qq.com']
    newsQQ_dicts = SiteQQCrawler.siteQQstarter(newsqq)
    newsthepaper = url_dict['www.thepaper.cn']
    newsThepaper_dicts = SiteThepaperCrawler.siteThepaperstarter(newsthepaper)
    return url_dict, news163_dicts, newsQQ_dicts, newsThepaper_dicts


if __name__ == '__main__':
    # url_dict = BingStarter(key_words=['化工爆炸', '化工泄露', '化工中毒', '化工火灾'])       # 需要外部starter传入关键字字段
    # url_dict = BingStarter(key_words=['化工爆炸', '化工泄露'])       # 需要外部starter传入关键字字段
    # 吊起门户网站爬虫和微博爬虫工作
    url_dict = {
        'news.163.com': [
            ('化工爆炸 site:news.163.com', '石家庄化工企业爆炸 目击者:以为发生地震 玻璃震碎_网易新闻',
             'https: //news.163.com/20/0509/08/FC63FB3V0001899O.html'),
            ('化工爆炸 site:news.163.com', '广西化工厂爆炸致4死6伤原因查明：5吨反应釜爆炸|爆炸|反应釜| …',
             'https: //news.163.com/19/1015/16/ERHSIUCU0001899N.html'),
            ('化工火灾 site:news.163.com', '公司拒发遣散费 工人开叉车3天碾坏3000台iPhone|遣散费|资方|苹 …',
             'https: //news.163.com/19/1217/01/F0IHDG1M0001875O.html'),
            ('化工火灾 site:news.163.com', '内蒙古消防救援总队举行国庆70周年 消防安全保卫跨区域实战拉动 …',
             'http: //hhht.news.163.com/19/0927/16/EQ3I3JUF04138EI3.html')],
        'news.qq.com': [
            ('化工爆炸 site:news.qq.com', '江苏响水天嘉宜化工有限公司“3-21”特别重大爆炸事故调查报告公 …',
             'https: //news.qq.com/a/20191115/007799.htm'),
            ('化工爆炸 site:news.qq.com', '广东珠海一石化厂发生爆炸：现场火光冲天 暂无人员伤亡_新闻_腾 …',
             'https: //news.qq.com/a/20200114/061719.htm'),
            ('化工爆炸 site:news.qq.com', '响水爆炸事故调查组：对责任人都要依法依规依纪严肃追责和惩 …',
             'https: //news.qq.com/a/20191113/009381.htm'),
        ],
        'www.thepaper.cn': [
            ('化工爆炸 site:www.thepaper.cn', '危化品爆炸警钟长鸣、旧疾新患亟待消除，国务院安委办暗访_绿 …',
             'https: //www.thepaper.cn/newsDetail_forward_8892087'),
            ('化工爆炸 site:www.thepaper.cn', '视频丨湖北仙桃市一化工厂锅炉爆炸，已致5伤4失联_直击现场_澎 …',
             'https: //www.thepaper.cn/newsDetail_forward_8564946'),
            ('化工火灾 site:www.thepaper.cn', '国家危化品应急救援吉林石化队与吉林市消防联合开展实战演练 提 …',
             'https: //www.thepaper.cn/newsDetail_forward_7242951'),
            ('化工火灾 site:www.thepaper.cn', '警惕！刚入四月：江苏一企业发生火灾致5人死亡_政务_澎湃新闻 …',
             'https: //www.thepaper.cn/newsDetail_forward_6869998'),
            ('化工火灾 site:www.thepaper.cn', '一周事故及安全警示（2020年第18期）_政务_澎湃新闻-The Paper',
             'https: //www.thepaper.cn/newsDetail_forward_7435023')]
    }

    news163 = url_dict['news.163.com']
    news163_dicts = Site163Crawler.site163starter(news163)
    newsqq = url_dict['news.qq.com']
    newsQQ_dicts = SiteQQCrawler.siteQQstarter(newsqq)
    newsthepaper = url_dict['www.thepaper.cn']
    newsThepaper_dicts = SiteThepaperCrawler.siteThepaperstarter(newsthepaper)








