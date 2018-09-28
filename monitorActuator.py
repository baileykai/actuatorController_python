import libactuatorController as actuatorController
import time
import _thread
import signal
import sys
from actuatorDefine import OperationFlags

flag = -1



def init():
    actuatorController.addOperationcallback(operationCallback)
    actuatorController.addAttrChangecallback(attrChangeCallback)
    actuatorController.addErrorCallback(errorCallback)
    actuatorController.initController(0)
    actuatorController.autoRecoginze()
    _thread.start_new_thread(process,())




def operationCallback(id,type):
   global flag
   flag = type
   if flag == OperationFlags['Recognize_Finished']:
       result = actuatorController.getActuatorIdArray()
       print("Number of connected actuators:%d"%(len(result)))
       actuatorController.launchAllActuators()


def attrChangeCallback(id,attr,value):
    print("attr")
    print("Actuator ID:%d" % (id))
    print("atribute ID:%s" % (attr))
    print("atribute value:%s"%(value))
    print("----------------------------")

def sigint_handler(signum, frame):
    actuatorController.closeAllActuators()
    sys.exit(0)


def errorCallback(type):
    print("error type: %s" % (type))

def process():
   while True:
       actuatorController.processEvents()
       time.sleep(0.1)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    init()
    input('')