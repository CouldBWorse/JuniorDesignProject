from GcodeParser import Parser
from positionHandler import posHandler
from StepperMotorLib import StepperMotor
import time

motor1 = StepperMotor(19,26,0.03)
motor2 = StepperMotor(20,21,0.03)
arm1 = 170
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []


def setUp(filename: str, homePos: tuple):
    exampleParse = Parser(filename, homePos)
    exampleParse.parse_gcode()
    exampleParse.defCmds()

    example = posHandler(exampleParse.positions,exampleParse.shortendCmds,arm1,arm2)
    example.calcAngles()
    print(example.angleList)
    

    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])


def run():
    for i in range(len(stps1)):
        time.sleep(0.5)
        intStp1 = int(stps1[i])
        intStp2 = int(stps2[i])
        motor1.goTo(intStp1)
        motor2.goTo(intStp2)
        

setUp('example.gcode',homePos)
run()