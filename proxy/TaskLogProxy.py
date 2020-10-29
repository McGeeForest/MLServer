import grpc
import proto_generate.tasklog_pb2 as pb2
import proto_generate.tasklog_pb2_grpc as pb2_grpc

def collectLog(taskId, message):

    try:
        channel = grpc.insecure_channel('localhost:5002')
        stub = pb2_grpc.TaskLogStub(channel)
        stub.collectLog(pb2.LogRequest(taskId=taskId, message=message))
    except:
        print('collect log connect error')