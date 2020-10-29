import grpc
import time
import proto_generate.server1_pb2_grpc as s1_pb2_grpc
import proto_generate.server2_pb2_grpc as s2_pb2_grpc
import proto_generate.taskmanage_pb2_grpc as tm_pb2_grpc
import proto_generate.taskcrawler_pb2_grpc as tc_pb2_grpc


from facade.Server1Facade import Server1Facade
from facade.Server2Facade import Server2Facade
from facade.TaskManageFacade import TaskManageFacade
from facade.TaskCrawlerFacade import TaskCrawlerFacade
from concurrent import futures

def run():
    crawler_server = grpc.server()
    tc_pb2_grpc.add_taskcrawlerServicer_to_server(TaskCrawlerFacade(), crawler_server)



    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # s1_pb2_grpc.add_Server1Servicer_to_server(Server1Facade(), grpc_server)
    # s2_pb2_grpc.add_Server2Servicer_to_server(Server2Facade(), grpc_server)
    # tm_pb2_grpc.add_TaskManageServicer_to_server(TaskManageFacade(), grpc_server)
    tc_pb2_grpc.add_taskcrawlerServicer_to_server(TaskCrawlerFacade(), grpc_server)
    grpc_server.add_insecure_port('[::]:5001')
    grpc_server.start()

    print('server started at localhost:5001')

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        grpc_server.stop(0)



if __name__ == '__main__':
    run()

