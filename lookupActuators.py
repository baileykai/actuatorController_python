import libactuatorController as actuatorController
import time
import _thread
import signal
import sys

flag = -1



#初始化
def init():
    #添加信号回调，会将信号返回到operationCallback函数中
    actuatorController.addOperationcallback(operationCallback)
    # 添加属性信息回调，会将属性返回到attrChangeCallback函数中
    actuatorController.addAttrChangecallback(attrChangeCallback)
    # 添加错误回调，会将错误返回到errorCallback函数中
    actuatorController.addErrorCallback(errorCallback)
    #进行初始化
    actuatorController.initController(0)
    #自动识别
    actuatorController.autoRecoginze()
    _thread.start_new_thread(process,())


def sigint_handler(signum, frame):
    actuatorController.closeAllActuators()
    sys.exit(0)


def operationCallback(id,type):
   global flag
   flag = type
   # flag 自动识别完成
   if flag == 0:
       result = actuatorController.getActuatorIdArray()
       print("Number of connected actuators:%d"%(len(result)))

#会返回执行器的属性
def attrChangeCallback(id,attr,value):
    return

#返回错误信息
def errorCallback(type):
    print("error type: %s" % (type))

#处理控制器事件，控制器所有的信号通知以及执行器属性刷新都依赖此函数的调用，所以不应该阻塞该函数的调用
def process():
   while True:
       actuatorController.processEvents()
       time.sleep(0.1)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    init()
    input('')