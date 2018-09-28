import libactuatorController as actuatorController
import time
import _thread
import signal
import sys
from actuatorDefine import ActuatorAttribute
flag = -1



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
       if actuatorController.getActuatorAttribute(result[0], ActuatorAttribute['ACTUATOR_SWITCH']) == 1:
           # 调整执行器速度环最小电流输出
           actuatorController.setMinOutputCurrent(result[0], -10);
           # 调整执行器速度环最大电流输出
           actuatorController.setMaxOutputCurrent(result[0], 10);
           # 调整执行器位置环最小速度输出
           actuatorController.setMinOutputVelocity(result[0], -2000);
           # 调整执行器位置环最大速度输出，最大值要大于最小值
           actuatorController.setMaxOutputVelocity(result[0], 2000);
           # 调整执行器Mode_Profile_Pos的最大速度（RPM）
           actuatorController.setActuatorAttribute(result[0], ActuatorAttribute['PROFILE_POS_MAX_SPEED'], 1000);




def attrChangeCallback(id,attr,value):
    description = ''
    actualValue = ''
    unitStr = ''
    if attr == ActuatorAttribute['VEL_OUTPUT_LIMITATION_MAXIMUM']  :
        description = "VEL_OUTPUT_LIMITATION_MAXIMUM"
        actualValue = actuatorController.getActuatorAttribute(id,ActuatorAttribute['CURRENT_SCALE'] )*value
        unitStr = "A"
    elif attr == ActuatorAttribute['VEL_OUTPUT_LIMITATION_MINIMUM']  :
        description = "VEL_OUTPUT_LIMITATION_MINIMUM"
        actualValue = actuatorController.getActuatorAttribute(id, ActuatorAttribute['CURRENT_SCALE'] )*value
        unitStr = "A"
    elif attr == ActuatorAttribute['POS_OUTPUT_LIMITATION_MAXIMUM'] :
        description = "POS_OUTPUT_LIMITATION_MAXIMUM"
        actualValue = actuatorController.getActuatorAttribute(id, ActuatorAttribute['VELOCITY_SCALE'] )*value
        unitStr = "RPM"
    elif attr == ActuatorAttribute['POS_OUTPUT_LIMITATION_MINIMUM'] :
        description = "POS_OUTPUT_LIMITATION_MINIMUM"
        actualValue = actuatorController.getActuatorAttribute(id, ActuatorAttribute['VELOCITY_SCALE'] )*value
        unitStr = "RPM"
    elif attr == ActuatorAttribute['PROFILE_POS_MAX_SPEED'] :
        description = "PROFILE_POS_MAX_SPEED"
        actualValue = value
        unitStr = "RPM"

    if description != '' :
        print("Actuator:%d %s change to %d %s" % (id,description,actualValue,unitStr))



def sigint_handler(signum, frame):
    actuatorController.closeAllActuators()
    sys.exit(0)


def errorCallback(type):
    print("error type: %s" %(type))


def process():
   while True:
       actuatorController.processEvents()
       time.sleep(0.1)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    init()
    input("")


