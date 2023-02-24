from GcodeParser import Parser
from positionHandler import posHandler
from StepperMotorLib import StepperMotor
import time


motor2 = StepperMotor(19,26)
motor1 = StepperMotor(20,21)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []
delay = 0.02

def setUp(filename: str, homePos: tuple):
    exampleParse = Parser(filename, homePos)
    exampleParse.parse_gcode()
    exampleParse.defCmds()

    example = posHandler(exampleParse.positions,exampleParse.shortendCmds,arm1,arm2)
    example.calcAngles()
    example.stepsList.insert(0,(0,0))
    print(example.stepsList)
    

    for tup in example.stepsList:
        stps1.append(int(tup[0]))
        stps2.append(int(tup[1]))
    
def run():
    for i in range(len(stps1)):
        motor1.goTo(stps1[i],delay)
        motor2.goTo(stps2[i],delay)
        print("Motor 1: " + str(motor1.Pos))
        print("Motor 2: " + str(motor2.Pos))
            
            


setUp('example2.gcode', homePos)
run()