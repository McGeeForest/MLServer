from selenium import webdriver
import urllib, requests, time
from bs4 import BeautifulSoup  # 处理抓到的页面
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}  # 定义头文件，伪装成浏览器





def starter(headers, key_words, page_count, listend_sites):
    # 1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
    browser = webdriver.Chrome()
    def sub_pages(browser, headers, key_words, page_count, listend_site):
        link_pair_list = []
        # 2.通过浏览器向服务器发送URL请求
        print(listend_site)
        url = 'https://www.baidu.com.cn/s?wd=' + urllib.parse.quote(' '.join(key_words)) # word为关键词，pn是百度用来分页的
        browser.get(url)
        print(url)
        # h1 = browser.window_handles
        # # 模拟筛选被监测网站 news.sina.com  news.sohu.com  news.qq.com  news.163.com
        # element = browser.find_element_by_xpath('//*[@id="container"]/div[2]/div/div[2]/div').click()
        # time.sleep(0.5)
        # element = browser.find_element_by_xpath('//*[@id="container"]/div[2]/div/div[1]/span[4]').click()
        # time.sleep(0.3)
        # element = browser.find_element_by_xpath('//*[@id="c-tips-container"]/div[3]/div/div/ul/li[1]/input').click()
        # time.sleep(0.2)
        # listend_site = list(listend_site)
        # for x in listend_site:
        #     browser.find_element_by_xpath('//*[@id="c-tips-container"]/div[3]/div/div/ul/li[1]/input').send_keys(x)
        #     time.sleep(0.1)
        # browser.find_element_by_xpath('//*[@id="c-tips-container"]/div[3]/div/div/ul/li[1]/a').click()
        browser.get(browser.current_url)
        for page in range(page_count-1):

            html_page = browser.page_source
            soup = BeautifulSoup(html_page, 'lxml')
            tagh3 = soup.find_all('h3')
            flut = 0

            for h3 in tagh3:
                flut += 1
                browser.set_window_size(1000+flut, 800+flut)
                href = h3.find('a').get('href')
                tltle = h3.find('a').text
                print(href)
                baidu_url = requests.get(url=href, headers=headers, allow_redirects=False)
                real_url = baidu_url.headers['Location']  # 得到网页原始地址
                if real_url.startswith('http'):
                    link_pair_list.append((tltle, real_url))
                # print("============")
            browser.find_element_by_xpath('// *[ @ id = "page"] / div / a[10]').click()
        return link_pair_list
    for listend_site in listend_sites:
        link_pair_list = sub_pages(browser, headers, key_words, page_count, listend_site)
        print(link_pair_list)

# element=browser.find_element_by_link_text("“下团组”时间")
# element.click()
# key_words = ['爆炸', '泄露','中毒', '火灾']
key_words = ['爆炸 泄露 中毒 site:news.163.com']
starter(headers,key_words=key_words[:2], page_count=5, listend_sites=['news.163.com'])



