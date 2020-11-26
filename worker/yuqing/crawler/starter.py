#coding:utf-8
import json
import sys, datetime
import pymongo
from pymongo.errors import DuplicateKeyError
from worker.yuqing.crawler.weibospider.settings import MONGO_HOST, MONGO_PORT
rootpath = sys.path.append("D:/OneDriveEdu/file/project/grpc_w2m_framework_m/worker/yuqing")
sys.path.append("D:/OneDriveEdu/file/project/grpc_w2m_framework_m/worker/yuqing/crawler/weibospider")
import worker.yuqing.crawler.bingspider.BingStarter as bingEntrance
import worker.yuqing.crawler.weibospider.run_spider as weiboEntrance
from worker.yuqing.crawler.weibospider.pipelines import MongoDBPipeline


import torch
import torch.nn.functional as F

class MongoDBPipeline_MenHu(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client['PublicNewsComments']
        self.Users = db["Users"]
        self.Tweets = db["OriginNews"]

    def process_item(self, item):
        # if spidername == 'tweet_spider':
        #     print(item)
        self.insert_item(self.Tweets, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            pass


class Logger(object):
    def __init__(self, filename='log.log'):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass

def run(key_words):
    sys.stdout = Logger('log-' + str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.log')
    # key_words = ['化工爆炸', '化工泄露', '化工中毒', '化工火灾']
    # 1.用于启动必应搜索和微博搜索
    # 2.将数据字段最后进行统一，存入数据库，现在暂定为json格式

    # 1.1 启动必应（必应吊起门户网站爬虫）
    pipeline = MongoDBPipeline_MenHu()
    # url_dict, news163_dicts, newsQQ_dicts, newsThepaper_dicts = bingEntrance.BingStarter(key_words=key_words)
    #
    # for item in news163_dicts:
    #     pipeline.process_item(item)
    # for item in newsQQ_dicts:
    #     pipeline.process_item(item)
    # for item in newsThepaper_dicts:
    #     pipeline.process_item(item)
    # print("**************result**************")
    # print(url_dict)
    # print(news163_dicts)
    # print(newsQQ_dicts)
    # print(newsThepaper_dicts)
    # 1.2 启动微博爬虫
    weiboEntrance.weiboStarter(key_words=key_words)
    return 'success'

class testModel(torch.nn.Module):
    def __init__(self):
        super(testModel, self).__init__()
        self.linear = torch.nn.Linear(in_features=3, out_features=2)
    def forward(self,x):
        x = self.linear(x)
        return x
    def num_flat_features(self,x):
        size=x.size()[1:] # all dimensions except the batch dimension
        num_features=1
        for s in size:
            num_features*=s
        return num_features

def runTest(key_words):
    net = testModel()
    net.forward(torch.FloatTensor([[1.0,2.0,3.0],[4.0,5.0,6.0]]))
    torch.save(net,"D:/testModel.pth")
    return 'success'


if __name__ == '__main__':
    sys.stdout = Logger('log-' + str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.log')
    key_words = ['化工爆炸', '化工泄露', '化工中毒', '化工火灾']
    # 1.用于启动必应搜索和微博搜索
    # 2.将数据字段最后进行统一，存入数据库，现在暂定为json格式

    # 1.1 启动必应（必应吊起门户网站爬虫）
    pipeline = MongoDBPipeline_MenHu()
    url_dict, news163_dicts, newsQQ_dicts, newsThepaper_dicts = bingEntrance.BingStarter(key_words=key_words)
#     newsThepaper_dicts = [json.loads(
#         s=str({
#     "news_title": "危化品爆炸警钟长鸣、旧疾新患亟待消除，国务院安委办暗访",
#     "news_author": "新华社",
#     "news_timeStamp": 1598437020,
#     "news_link": "https://www.thepaper.cn/newsDetail_forward_8892087",
#     "news_content": "新华社北京8月26日消息，我国是世界化工大国，涉及危化品的场所大量存在。危化品在生产生活中必不可少，但需严格管理。近期黎巴嫩贝鲁特重大爆炸事件，再次敲响警钟。国务院安委办8月7日至17日迅即开展了明察暗访行动，检查对象是硝酸铵等爆炸性重点管控化学品生产、储存企业及港口货场。6个检查组赶赴11个重点省份，深入检查80家企业，共发现问题隐患423项，其中重大隐患42项、停产整顿企业12家。数字背后，暴露出一幕幕触目惊心的危险情形，一处处亟待消除的旧疾新患。隐患一：违规储存随意销售国内外曾多次发生过硝酸铵爆炸导致人员伤亡事故。应急管理部有关负责人介绍，硝酸铵主要用途是制作炸药和肥料，但由于其危险性，2002年9月30日起我国将硝酸铵纳入民用爆炸物品管理，不得直接作为化肥生产销售。2020年5月，应急管理部、工信部、公安部和交通运输部联合公告，将硝酸铵列入《特别管控危险化学品目录（第一版）》。然而，检查组发现，对于这样一种爆炸性危化品，一些企业风险意识淡薄，违规堆存、随意销售。例如，在山西天脊煤化工集团股份有限公司，该企业把面积达2000平方米的铁路危货装车站台用作中转站，存放大量硝酸铵，且未按照硝酸铵专用仓库管理。红河恒林化工有限公司虽取得危化品安全使用许可证，许可范围为农用硝酸铵，而其2020年共签订700吨多孔硝酸铵的采购合同，而多孔硝酸铵多用以制作炸药。检查组有关负责人认为，违规堆存、随意销售，与产能过剩有一定关系。全国现有硝酸铵生产企业40家，年产能约1000万吨，2019年产量约590万吨，全国实际年需求量约500万吨，且主要用于民爆物品生产。检查组建议，合理规划硝酸铵产业布局，调整生产企业产品结构，增加安全性较高的液态硝酸铵产量，并鼓励硝酸铵和民爆物品生产企业上下游一体化发展，硝酸铵产品就地就近转化，减少储运环节安全风险。同时，严格限制新建、扩建硝酸铵建设项目。隐患二：产品包装不规范、不完整硝酸铵产品包装标识内容不规范、不完整，“一书一签”制度不落实，会严重影响化学品安全信息的有效传递。由此导致的操作错误、防范失误，屡次成为引发事故的“元凶”。检查组发现，上述问题仍在一些企业存在。山西金恒化工集团股份有限公司是一家以硝酸铵为原料，生产民爆物品的企业。在其固体硝酸铵存放库，由山西中煤平朔能源化工有限公司等生产的两类硝酸铵产品包装上，均未告知产品有爆炸危险，未写明遇高温、撞击等会发生爆炸。检查组建议，严格规范硝酸铵等爆炸性重点管控化学品“一书一签”制度的执行落实，硝酸铵产品包装应注明爆炸危险性，将危险特性和处置要求等安全信息及时准确全面传递给下游企业、用户、使用人员以及应急处置人员。隐患三：安全管理存漏洞高危企业的安全管理，本应高标准、高水平。但检查组发现，不少企业在这方面存在漏洞，比如动火、进入受限空间作业等特殊作业环节的安全管理，可燃和有毒气体监测报警设施管理、应急和消防设施维护等。检查组有关负责人表示，各地要组织开展针对性执法检查，并探索在涉及特别管控危化品的企业实施作业全过程录像制度，视频保存3个月以上备查。检查组还发现一个新情况：一些地方要求对危废仓库实行封闭管理，而对可能带来的易燃易爆、有毒有害气体集聚风险重视不够；企业对危废仓库，往往投入不舍得、检查不上心，相关设施设备普遍缺乏、安全管理无人问津。对此，检查组建议，各级安委办要协调相关部门加强对危废仓库监管，对属性不明危废进行鉴别鉴定，同时建立完善环保设施安全评估评价机制，严防在环境污染防治中产生新的安全风险。隐患四：贪图便利瞒报匿报天津港、上海港、青岛港、宁波港，是此次明察暗访的4个重点港口。检查组有关负责人表示，目前，天津港已不再开展硝酸铵类等爆炸品的所有作业，上海港硝酸铵作业量较小，青岛港及港区内6家港口企业具有硝酸铵经营资质，宁波港12家港口企业具有硝酸铵经营资质，但上述港区不涉及硝酸铵储存的场所。检查组发现，各大港区对危货的安全管理，正朝着数字化智能化加速迈进。然而，危险品瞒报、匿报、夹带等行为，令人防不胜防。例如，多家企业反映，一些托运人出于控制成本、贪图便利等目的，将危货申报为普通货物，将危险性高的危货申报为危险性低的危货，在普通货物中夹带危货等问题。这些行为往往不易被及时发现，大大增加了集装箱运输、装卸和储存的安全风险。对此，有关港口企业建议，应当修改完善有关法律法规，加大对违法违规托运人的处罚力度。（原题为：《危化品爆炸警钟长鸣，旧疾新患岂能熟视无睹？——一份来自国务院安委办的明察暗访报告》）(本文来自澎湃新闻，更多原创资讯请下载“澎湃新闻”APP)",
#     "news_comments": [],
#     "news_site": "www.thepaper.cn"
# }).replace("'", '"'))]
    for item in news163_dicts:
        pipeline.process_item(item)
    for item in newsQQ_dicts:
        pipeline.process_item(item)
    for item in newsThepaper_dicts:
        pipeline.process_item(item)
    # print("**************result**************")
    # print(url_dict)
    # print(news163_dicts)
    # print(newsQQ_dicts)
    # print(newsThepaper_dicts)
    # 1.2 启动微博爬虫
    weiboEntrance.weiboStarter(key_words=key_words)

