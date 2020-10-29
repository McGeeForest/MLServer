import grpc

import proto_generate.server1_pb2 as s1_pb2
import proto_generate.server2_pb2 as s2_pb2
import proto_generate.server1_pb2_grpc as s1_pb2_grpc
import proto_generate.server2_pb2_grpc as s2_pb2_grpc


def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:5001')
    # 调用 rpc 服务
    stub1 = s1_pb2_grpc.Server1Stub(channel)
    response = stub1.fun1(s1_pb2.Fun1Request(taskId='123s', param='p1'))
    print("S1 client received: " + response.message)


    # 调用 rpc 服务
    stub2 = s2_pb2_grpc.Server2Stub(channel)
    response = stub2.fun2(s2_pb2.Fun2Request(taskId='124s', param='p2'))
    print("S2 client received: " + response.message)

    # channel = grpc.insecure_channel('localhost:5001')
    # # 调用 rpc 服务
    # stub = s1_pb2_grpc.Server1Stub(channel)
    # response = stub.fun1(s1_pb2.Fun1Request(taskId='123s'))
    # print("S1 client received: " + response.message)

if __name__ == '__main__':
    run()