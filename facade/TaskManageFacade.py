import grpc
import threading
import ctypes
import inspect
import proto_generate.taskmanage_pb2 as pb2
import proto_generate.taskmanage_pb2_grpc as pb2_grpc

class TaskManageFacade(pb2_grpc.TaskManageServicer):

    def listActiveTask(self, request, context):
        tasks = []
        for t in threading.enumerate():
            if t.name.startswith('Q49A_'):
                print(t.name)
                tasks.append(t.name[5:])
        return pb2.ListActiveReply(tasks = tasks)


    def killTask(self, request, context):
        threadName = 'Q49A_'+request.taskId
        for t in threading.enumerate():
            if t.name.__eq__(threadName):
                self.stopThread(t.ident)
                break
        return pb2.KillReply(message='')

    def stopThread(self, tid):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        exctype = SystemExit
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")