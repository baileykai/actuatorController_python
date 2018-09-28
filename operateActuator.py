import libactuatorController as actuatorController
import time
import _thread
import signal
import sys

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
   if flag == 0:
       result = actuatorController.getActuatorIdArray()
       print("Number of connected actuators:%d"%(len(result)))


def attrChangeCallback(id,attr,value):
    return


def errorCallback(type):
    print("error type: %s" % (type))

def process():
   while True:
       actuatorController.processEvents()
       time.sleep(0.1)

def char_to_directive(directive,value):
    result = actuatorController.getActuatorIdArray()
    if directive == 'v':
        actuatorController.setVelocity(int(result[0]), float(value))
    elif directive == 'c':
        actuatorController.setCurrent(int(result[0]), float(value))
    elif directive == 'p':
        actuatorController.setPosition(int(result[0]), float(value))
    elif directive == 'a':
        actuatorController.activeActuatorMode(int(value))
    elif directive == 'l':
        actuatorController.launchAllActuators()
    elif directive == 's':
        actuatorController.closeAllActuators()

def sigint_handler(signum, frame):
    actuatorController.closeAllActuators()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    init()
    while True:
        directive,value= input().split()
        char_to_directive(directive,value)