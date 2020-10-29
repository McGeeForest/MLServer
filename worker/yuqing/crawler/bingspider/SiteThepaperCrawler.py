import requests, time, json, re
from urllib import parse
from bs4 import BeautifulSoup as bs

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def get_comments(news_link, news_comments, api_param):
    cont_id = news_link.split('forward_')[1]
    api = 'https://www.thepaper.cn/newDetail_commt.jsp'
    if api_param['pageidx'] > 1:
        api = 'https://www.thepaper.cn/load_moreFloorComment.jsp'
    comments_response = requests.get(url=api, params=api_param)
    comments_soup = bs(comments_response.text, 'lxml')
    comments_list = comments_soup.select('div.comment_que > div > div.aqwright > div.ansright_cont > a')
    date_list = comments_soup.select('div.comment_que > div > div.aqwright > h3 > span')
    userid_and_commentid = comments_soup.select('div.comment_que > div > div.aqwleft > div > a')
    # print(len(comments_list), len(date_list), len(userid_and_commentid))

    news_comments_contents = [str(comment.text).replace("\n", '').replace(" ", '') for comment in comments_list]
    news_comments_dates = [str(news_comments_date.text) for news_comments_date in date_list]
    # print(news_comments_dates)
    p1 = re.compile(pattern='(?<=userId=).*?(?=&)', flags=re.IGNORECASE)       # 最小匹配，获得userid
    news_comments_userids = [re.findall(p1, str(userid_and_commentid.get('href')))[0] for userid_and_commentid in userid_and_commentid]
    p2 = re.compile(pattern='(?<=commentId=).*?(?=&)', flags=re.IGNORECASE)       # 最小匹配，获得userid
    # print(userid_and_commentid)
    news_comments_commentids = [re.findall(p2, str(userid_and_commentid.get('href'))+"&")[0] for userid_and_commentid in userid_and_commentid]      # 获得commentid
    # print(news_comments_commentids)
    # print(userid_and_commentid)
    for i in range(len(news_comments_contents)):
        item_news_comments = {}
        item_news_comments['comment_id'] = news_comments_commentids[i]
        item_news_comments['comment_userid'] = news_comments_userids[i]
        item_news_comments['comment_datetime'] = int(time.mktime(time.strptime(str(news_comments_dates[i]), "%Y-%m-%d")))
        item_news_comments['comment_content'] = news_comments_contents[i]
        news_comments.append(item_news_comments)
    print(news_comments)



    # # startId1
    # for comment in comments_list:
    #     if str(comment).startswith("回复@"):
    #         comment = comment.split(":")[1]

    # 组装递归爬取的api
    css_selecter = '#startId' + str(api_param['pageidx'])
    api_param['startId'] = comments_soup.select(css_selecter)[0].get('startid')
    api_param['pageidx'] += 1
    # print(css_selecter, api_param)
    if api_param['startId'] == '0':
        return news_comments
    return get_comments(news_link, news_comments, api_param)





def siteThepapercrawler(url):

    try:
        print('www.thepaper.cn:', url)
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        news_link = url
        news_title = soup.select('div.newscontent > h1')[0].text
        # print(news_title)

        time_author = ' '.join([soup.select('div.newscontent > div.news_about > p')[i].text for i in range(len(soup.select('div.newscontent > div.news_about > p')))]).replace("\n", '').split(" ")
        idate = ''
        itime = ''
        news_author = ''
        # 获取发布时间和新闻来源，太恶心了，真的太恶心了...判断有汉字的为来源，-分隔开长度是3的是日期，:分隔开长度是2的判断为时间
        for i in time_author:
            if len(i.split("-")) == 3:
                idate = i
            elif len(i.split(":")) == 2:
                itime = i
            elif is_chinese(i):
                news_author = i
        news_time = idate + ' ' + itime
        real_author = soup.select('div.newscontent > div.news_paike_author.clearfix > a > div.name')
        if len(real_author) != 0:     # 然后如果是澎湃号的内容，来源更改为其澎湃号
            news_author = real_author[0].text
        news_author = news_author.replace("来源：", '')
        # # 转换为时间戳
        timeArray = time.strptime(str(news_time), "%Y-%m-%d %H:%M")
        news_timeStamp = int(time.mktime(timeArray))
        # print(news_author, news_time, news_timeStamp)

        news_site = 'www.thepaper.cn'
        news_content = str(soup.select('div.newscontent > div.news_txt')[0].text)
        news_comments = []
        cont_id = news_link.split('forward_')[1]
        page_index = 1
        api_param = {
            'contid': cont_id,  # 文章id
            'startId': '',  # 第一条评论的id，可以为空，一次获得10条评论
            'pageidx': page_index
        }
        news_comments = get_comments(news_link, news_comments, api_param)
        # print('全部评论：', news_comments)

        # print(json.dumps(news_comments, ensure_ascii=False))
        # 转换为时间戳
        timeArray = time.strptime(str(news_time), "%Y-%m-%d %H:%M")
        news_timeStamp = int(time.mktime(timeArray))

    except Exception:
        print(Exception)
        return {"Exception": str(Exception)}
    # print(news_timeStamp)
    # print(news_title, news_time, news_author, news_timeStamp, news_link)
    # print(news_content)

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

def siteThepaperstarter(newsthepaper):
    print("澎湃新闻数据：")
    url_list = [newsthepaper[i][2].replace(" ", "") for i in range(len(newsthepaper))]
    news_dicts = [siteThepapercrawler(url_list[i]) for i in range(len(url_list))]
    print("爬取列表：", url_list)
    print(json.dumps(news_dicts[0], ensure_ascii=False))       # 最终结果的一项
    print("==================================================")
    return news_dicts

if __name__ == '__main__':

    url_list = ['https://www.thepaper.cn/newsDetail_forward_8892087', 'https://www.thepaper.cn/newsDetail_forward_6354204','https://www.thepaper.cn/newsDetail_forward_8806279','https://www.thepaper.cn/newsDetail_forward_3180260']
    siteThepapercrawler(url_list[2])






