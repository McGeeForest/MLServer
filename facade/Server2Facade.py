
import grpc
import proto_generate.server2_pb2 as pb2
import proto_generate.server2_pb2_grpc as pb2_grpc

class Server2Facade(pb2_grpc.Server2Servicer):
    # 重写fun2 方法
    def fun2(self, request, context):
        taskId = request.taskId
        param = request.param
        print("receive taskId: " + request.taskId + "  and param: " + request.param)

        msg = 'Server2 TaskId is {0} and param is {1}.'.format(taskId, param)
        return pb2.Fun2Reply(message = msg)
