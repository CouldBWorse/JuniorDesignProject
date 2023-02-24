from GcodeParser import Parser
from positionHandler import posHandler
from dualStepperMotor import dualMotor
import time
import multiprocessing

motors = dualMotor(20 , 21, 19, 26)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []
delay = 0.03

def setUp(filename: str, homePos: tuple):
    exampleParse = Parser(filename, homePos)
    exampleParse.parse_gcode()
    exampleParse.defCmds()

    example = posHandler(exampleParse.positions,exampleParse.shortendCmds,arm1,arm2)
    example.calcAngles()
    example.stepsList.insert(0,(0,0))
    print(example.stepsList)
    

    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])
    
def run():
    for i in range(len(stps1)):
        motors.goTo(int(stps1[i]),int(stps2[i]), delay)
        print("Motor Positions: (" + str(motors.Pos1) + ", " + str(motors.Pos2) +" )")
        time.sleep(1)

if __name__=="__main__":
    setUp('example.gcode',homePos)
    run()