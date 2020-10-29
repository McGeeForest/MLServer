
import grpc
import threading
import time
import proto_generate.taskcrawler_pb2 as pb2
import proto_generate.taskcrawler_pb2_grpc as pb2_grpc

import worker.yuqing.crawler.starter as starter

from proxy.TaskLogProxy import collectLog

class TaskCrawlerFacade(pb2_grpc.taskcrawlerServicer):
    # 重写fun1 方法
    def crawler1(self, request, context):
        taskId = request.taskId
        keywords = request.keywords
        print("receive taskId: " + request.taskId + "  and keywords: " + request.keywords)

        thread_name = "Q49A_{0}".format(taskId)
        # self.work(taskId, keywords)
        t = threading.Thread(target=self.work, args=(taskId, keywords), name=thread_name)
        t.start()

        #msg = 'Server1 TaskId is {0} and param is {1}.'.format(taskId, param)
        # msg = 'Task is run in backend'
        return pb2.Crawler1Reply(message = t.start())


    def work(self, taskId, param):
        msg = starter.run(eval(param))
        # t = threading.current_thread()
        #
        # for i in range(1, 600000):
        #     # 当前线程名
        #
        #     print("第{0}次执行线程 {1} taskId {2} param {3}".format(i, t.name, taskId, param))
        #     print(t)
        #
        #     msg = "第{0}次执行线程 {1} taskId {2} param {3}".format(i, t.name, taskId, param)
        #     collectLog(taskId, msg)
        #
        #     # 线程休眠
        #     time.sleep(1)
        # print("线程{0}执行完成".format(t.name))
        return msg