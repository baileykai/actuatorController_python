import libactuatorController as actuatorController
import time
import _thread
import signal
import sys
from actuatorDefine import ActuatorAttribute
flag = -1
bSetLimitation = False;


#初始化
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
       actuatorController.launchAllActuators()
   elif flag == 1 :
       result = actuatorController.getActuatorIdArray()
       print("Number of connected actuators:%d" % (len(result)))
       if actuatorController.getActuatorAttribute(result[0], ActuatorAttribute['ACTUATOR_SWITCH']) == 1:
           global bSetLimitation
           actuatorController.setHomingPosition(id,  actuatorController.getActuatorAttribute(id, ActuatorAttribute['ACTUAL_POSITION']))
           actuatorController.setMinPosLimitValue(id, -10)
           actuatorController.setMaxPosLimitValue(id, 10)
           actuatorController.setActuatorAttribute(id, ActuatorAttribute['POS_OFFSET'], 0.5)
           bSetLimitation = True



nResponse = 0
min = 0
max = 0
offset = 0
def attrChangeCallback(id,attr,value):
    if bSetLimitation == False :
        return

    global nResponse
    global min
    global max
    global offset
    if attr == ActuatorAttribute['HOMING_POSITION']:
        nResponse = nResponse + 1
    elif attr == ActuatorAttribute['POS_LIMITATION_MINIMUM'] :
        min = value;
        nResponse = nResponse + 1
    elif attr == ActuatorAttribute['POS_LIMITATION_MAXIMUM'] :
        max = value;
        nResponse = nResponse + 1
    elif attr == ActuatorAttribute['POS_OFFSET'] :
        offset = value;
        nResponse = nResponse + 1


    if nResponse == 4 :
        if max-min-2*offset > 0 :
            print("Set Limitation successfully! The actuator's range of movement is : %f %f" % (min+offset,max-offset))
        else :
            print(" Set Limitation failed!  Minimum: %f  Maximum: %f Offset: %f" % (min,max,offset))




def sigint_handler(signum, frame):
    actuatorController.closeAllActuators()
    sys.exit(0)


#错误回调函数，打印出错误类型
def errorCallback(type):
    print("error type: %s" % (type))

#
def process():
   while True:
       actuatorController.processEvents()
       time.sleep(0.1)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    init()
    input("")


