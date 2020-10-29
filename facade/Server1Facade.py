
import grpc
import threading
import time
import proto_generate.server1_pb2 as pb2
import proto_generate.server1_pb2_grpc as pb2_grpc

from proxy.TaskLogProxy import collectLog

class Server1Facade(pb2_grpc.Server1Servicer):
    # 重写fun1 方法
    def fun1(self, request, context):
        taskId = request.taskId
        param = request.param
        print("receive taskId: " + request.taskId + "  and param: " + request.param)

        thread_name = "Q49A_{0}".format(taskId)
        t = threading.Thread(target=self.work, args=(taskId, param), name=thread_name)
        t.start()

        #msg = 'Server1 TaskId is {0} and param is {1}.'.format(taskId, param)
        msg = 'Task is run in backend'
        return pb2.Fun1Reply(message = msg)


    def work(self, taskId, param):
        t = threading.current_thread()
        for i in range(1, 600000):
            # 当前线程名

            print("第{0}次执行线程 {1} taskId {2} param {3}".format(i, t.name, taskId, param))
            print(t)

            msg = "第{0}次执行线程 {1} taskId {2} param {3}".format(i, t.name, taskId, param)
            collectLog(taskId, msg)

            # 线程休眠
            time.sleep(1)
        print("线程{0}执行完成".format(t.name))
