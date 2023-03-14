from GcodeParser import Parser
from positionHandler import posHandler
from dualStepperMotor import dualMotor
from gpiozero import Servo
import time


motors = dualMotor(6, 5, 9, 11)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,1)
stps1 = []
stps2 = []
servoLst = []
delay = 0.02
cmds = []

servo_pin = 13
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
        
    for i in range(len(exampleParse.shortendCmds)):
        cmds.append(exampleParse.shortendCmds[i])
    
    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])

        
    print(example.stepsList)
    print(servoLst)
    print(cmds)
        
    
def run():
    for i in range(len(stps1)):
        servo.value = servoLst[i]
        time.sleep(1)
        motors.goTo(int(stps1[i]),int(stps2[i]), delay)
        print("Motor Positions: (" + str(motors.Pos1) + ", " + str(motors.Pos2) +" )")
        if cmds[i-1] == 'M6':
            toolChange = input("Press keyboard to continue")
        time.sleep(1)

if __name__=="__main__":
    setUp('TwoSquares.gcode',homePos)
    run()
