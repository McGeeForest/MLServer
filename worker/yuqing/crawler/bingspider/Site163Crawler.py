import requests, time, json
from bs4 import BeautifulSoup as bs
def site163crawler(url):

    try:
        print('news.163.com:', url)
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        news_link = url
        news_title = soup.select('#epContentLeft > h1')[0].text
        time_author = list(soup.select('#epContentLeft > div.post_time_source')[0].strings)
        temp_time = time_author[0].replace(" ", '').replace("\u3000", '').replace("\n", '').replace("来源:", '')
        news_time = temp_time[:10] + ' ' + temp_time[10:]
        news_site = 'news.163.com'
        news_author = time_author[1]
        # news_content = str(soup.select('#endText > p')[0].text).split('(function ()')[0].replace('\n','').replace(' ','')

        news_content = ""
        for p_content in soup.select('#endText > p'):
            if str(p_content).startswith("<p class="):
                continue
            if (str(p_content.string).replace("\n", "").replace(" ", "") == "None")|(str(p_content.string).replace("\n", "").replace(" ", "").endswith('Fragment')):
                continue
            news_content = news_content + str(p_content.string).replace("\n", "").replace(" ", "")
            # print(news_content)

        # news_comments_link = soup.select('#post_comment_area > div.post_comment_toolbar > div.post_comment_joincount > a')[0] # 拿不到
        news_comments_link = "http://comment.tie.163.com/" + news_link.split('/')[-1]
        # http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/EHA8I38S0001899N/comments/newList?limit=30&offset = 0
        comments_param = {
            "limit": 30,
            "offset": 0
        }
        # print(news_link.split('/')[-1])
        comments_api = 'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/' + str(news_link.split('/')[-1]).replace('.html', '') + '/comments/newList'
        comments_response = requests.get(url=comments_api, params=comments_param)
        comments = json.loads(comments_response.text)
        comments_list_num = comments.get("newListSize")     # 跟帖列表的数量
        temp_news_comments = comments.get("comments")
        # print('共有跟帖列表：' + str(comments_list_num) + ' 条')
        # print('本次请求获得：' + str(len(comments.get("commentIds"))) + ' 条')
        pages = comments_list_num//comments_param["limit"]  # 要请求的次数，除去第一次请求之后，还有请求的次数
        for page in range(pages):
            comments_param["offset"] = comments_param["limit"] * (page+1)
            comments_response = requests.get(url=comments_api, params=comments_param)
            comments = json.loads(comments_response.text)
            # print('本次请求获得：' + str(len(comments.get("commentIds"))) + ' 条')
            temp_news_comments.update(comments.get("comments"))
        # print(json.dumps(temp_news_comments, ensure_ascii=False))
        news_comments = []
        for comments_id in dict(temp_news_comments).keys():
            comment_item = {}
            temp_comment_item = temp_news_comments[comments_id]
            comment_item['comment_id'] = comments_id
            comment_item['comment_content'] = temp_comment_item['content']
            comment_item['comment_datetime'] = int(time.mktime(time.strptime(str(temp_comment_item['createTime']), "%Y-%m-%d %H:%M:%S")))
            comment_item['comment_userid'] = temp_comment_item['user']['userId']
            news_comments.append(comment_item)
        # print(news_comments)
        # 转换为时间戳
        timeArray = time.strptime(str(news_time), "%Y-%m-%d %H:%M:%S")
        news_timeStamp = int(time.mktime(timeArray))
    except Exception:
        print(Exception)
        return {"Exception": str(Exception)}
    # print(news_title, news_time, news_author, news_timeStamp, news_link, news_comments_link)
    # print(news_content)

    news_dict = {
        "news_title":news_title,
        # "news_time":news_time,
        "news_author":news_author,
        "news_timeStamp":news_timeStamp,
        "news_link":news_link,
        "news_comments_link":news_comments_link,
        "news_content":news_content,
        "news_comments":news_comments,
        "news_site":news_site
    }
    return news_dict
    # timeArray = time.localtime(timeStamp)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)


# 上层调用使用，传入三元组list （site，title，url）
def site163starter(news163):
    print("网易新闻数据：")
    url_list = [news163[i][2].replace(" ", "") for i in range(len(news163))]
    news_dicts = [site163crawler(url_list[i]) for i in range(len(url_list))]
    print("爬取列表：", url_list)
    print(json.dumps(news_dicts[0], ensure_ascii=False))       # 最终结果的一项
    print("==================================================")
    return news_dicts

if __name__ == '__main__':
    url_list = ['https://news.163.com/19/1015/16/ERHSIUCU0001899N.html',
                'http://news.163.com/40725/5/0S56O6560001122B.html',
                'https://news.163.com/20/0913/14/FMDMTF3B0001899O.html',
                'https://news.163.com/19/1229/10/F1ICMFHK0001899O.html',
                'https://news.163.com/20/0509/08/FC63FB3V0001899O.html']
    site163crawler(url_list[0])






