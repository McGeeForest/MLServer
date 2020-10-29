import requests, time, json
from bs4 import BeautifulSoup as bs
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}  # 定义头文件，伪装成浏览器

def siteQQcrawler(url):

    try:
        print('news.qq.com:', url)
        response = requests.get(url)
        # print(response.text)
        soup = bs(response.text, 'lxml')
        news_link = url
        news_title = soup.select('#Main-Article-QQ > div > div.qq_main > div.qq_article > div.hd > h1')[0].text
        news_time = soup.select('#Main-Article-QQ > div > div.qq_main > div.qq_article > div.hd > div > div.a_Info > span.a_time')[0].text
        # 转换为时间戳
        timeArray = time.strptime(str(news_time), "%Y-%m-%d %H:%M")
        news_timeStamp = int(time.mktime(timeArray))
        news_site = 'news.qq.com'
        news_author = soup.select('#Main-Article-QQ > div > div.qq_main > div.qq_article > div.hd > div > div.a_Info > span.a_source')[0].text
        news_content = ""
        for p_content in soup.select('#Cnt-Main-Article-QQ > p'):
            news_content = news_content + str(p_content.text).replace("\n", "").replace(" ", "")

        # news_comments_link = soup.select('#post_comment_area > div.post_comment_toolbar > div.post_comment_joincount > a')[0] # 拿不到
        page_params = str(soup.select('#Main-Article-QQ > div > div.qq_main > div.qq_articleFt > script')[0].text).replace(' ', '').replace('\n', '').split(';')
        comments_api = ''
        # news_item_id = ''
        for item in page_params:        # 取新闻的id，用于组装评论请求api
            if item.startswith('cmt_id='):
                # news_item_id = item.split("=")[1]
                comments_api = 'https://coral.qq.com/article/' + item.split("=")[1] + '/comment/v2'
                break
        # https: // coral.qq.com / article / 4414639487 / comment / v2?callback = _article4414639487commentv2 & orinum = 10 & oriorder = t & pageflag = 1 & cursor = 6601096829631067708 & scorecursor = 0 & orirepnum = 2 & reporder = o & reppageflag = 1 & source = 1

        # http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/EHA8I38S0001899N/comments/newList?limit=30&offset = 0
        # print(news_title, news_time, news_author, news_content, comments_api)
        comments_param = {
            "orinum": 30,
            "oriorder": 't',
            'cursor': 0,
            'source': 1,
            'pageflag': 1,
            'scorecursor': 0,
            'orirepnum': 2,
            'reporder': 'o',
            'reppageflag': 1
            # 'callback': '_article' + 4414639487 + 'commentv2'
        }
        sub_oricomments_length = 1000
        temp_news_comments = []
        while sub_oricomments_length > 29:     # 获得所有的评论，每次请求30条原始评论以及他们的回复
            comments_response = requests.get(url=comments_api, params=comments_param, headers=headers)
            # print(comments_response.text)
            comments = json.loads(comments_response.text)
            # print(comments)
            if comments.get('errCode') != 0:     # 没有请求到的话，继续请求
                continue

            last = comments.get("data").get("last")     # 取到下次请求的参数cursor
            sub_oricomments_list = comments.get("data").get("oriCommList")       # 本次请求的原始评论的json， 下面得到回复的评论

            sub_repcomments_list = []
            # print(comments.get("data").get("repCommList"))
            temp_sub_repcomments_list = dict(comments.get("data").get("repCommList")).values()
            for sub_repcomments_item in temp_sub_repcomments_list:
                sub_repcomments_list = sub_repcomments_list + sub_repcomments_item
            # print(sub_repcomments_list)
            sub_comments = sub_oricomments_list + sub_repcomments_list
            temp_news_comments += sub_comments       # 全部的评论 包括原始评论和回复评论
            # print(sub_comments)
            sub_oricomments_length = len(sub_oricomments_list)
            comments_param['cursor'] = last
            # print(last, sub_oricomments_length)
        # print(json.dumps(temp_news_comments[0], ensure_ascii=False))
        news_comments = []
        for temp_comment_item in temp_news_comments:
            comment_item = {}
            comment_item['comment_id'] = temp_comment_item['id']
            comment_item['comment_content'] = temp_comment_item['content']
            comment_item['comment_datetime'] = temp_comment_item['time']
            comment_item['comment_userid'] = temp_comment_item['userid']
            news_comments.append(comment_item)
        print(news_comments)
    except Exception:
        print(Exception)
        return {"Exception": str(Exception)}
        # return None

    # print(news_title,news_time,news_timeStamp,news_author,news_content,news_site,news_link)
    # print(news_comments)

    news_dict = {
        "news_title":news_title,
        # "news_time":news_time,
        "news_author":news_author,
        "news_timeStamp":news_timeStamp,
        "news_link":news_link,
        # "news_comments_link":news_comments_link,
        "news_content":news_content,
        "news_comments":news_comments,
        "news_site":news_site
    }
    return news_dict
    # timeArray = time.localtime(timeStamp)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)

def siteQQstarter(newsqq):
    print("腾讯新闻数据：")
    url_list = [newsqq[i][2].replace(" ", "") for i in range(len(newsqq))]
    news_dicts = [siteQQcrawler(url_list[i]) for i in range(len(url_list))]
    print("爬取列表：", url_list)
    # print(json.dumps(news_dicts[0], ensure_ascii=False))       # 最终结果的一项
    print("==================================================")
    return news_dicts

if __name__ == '__main__':
    url_list = ['https://news.qq.com/a/20200114/061719.htm', 'http://news.qq.com/a/20191115/007799.htm', 'https://news.qq.com/a/20191113/009381.htm', 'http://news.qq.com/a/20091227/000049.htm', 'http://bb.news.qq.com/a/20080124/000030.htm', 'http://news.qq.com/a/20091227/000049.htm', 'http://bb.news.qq.com/a/20110222/000016.htm', 'http://bb.news.qq.com/zt2010/fysp/index.htm', 'http://bb.news.qq.com/a/20101104/000039.htm']
    news_dicts = [siteQQcrawler(url_list[i]) for i in range(len(url_list))]
    print("爬取列表：", url_list)
    print(news_dicts)
    print(json.dumps(news_dicts[0], ensure_ascii=False))  # 最终结果的一项
    print("==================================================")
