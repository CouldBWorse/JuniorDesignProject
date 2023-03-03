from GcodeParser import Parser
from positionHandler import posHandler
from dualStepperMotor import dualMotor
from gpiozero import Servo
import time


motors = dualMotor(20 , 21, 19, 26)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []
servoLst = []
delay = 0.03

servo_pin = 17
servo = Servo(servo_pin)

def setUp(filename: str, homePos: tuple):
    exampleParse = Parser(filename, homePos)
    exampleParse.parse_gcode()
    exampleParse.defCmds()

    example = posHandler(exampleParse.positions,exampleParse.shortendCmds,arm1,arm2)
    example.calcAngles()
    example.stepsList.insert(0,(0,0))
    example.servoList.insert(0,1)


    for i in range(len(example.servoList)):
        servoLst.append(example.servoList[i])
    
    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])
        
    print(example.stepsList)
    print(servoLst)
        
    
def run():
    for i in range(len(stps1)):
        servo.value = servoLst[i]
        motors.goTo(int(stps1[i]),int(stps2[i]), delay)
        print("Motor Positions: (" + str(motors.Pos1) + ", " + str(motors.Pos2) +" )")
        time.sleep(1)

if __name__=="__main__":
    setUp('example.gcode',homePos)
    print(stps1)
    run()