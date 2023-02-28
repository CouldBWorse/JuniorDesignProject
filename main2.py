from GcodeParser import Parser
from positionHandler import posHandler
from dualStepperMotor import dualMotor
import time
from servoSetup import Setup

motors = dualMotor(20 , 21, 19, 26)
servo = Setup(17,0)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []
servoLst = []
delay = 0.03

def setUp(filename: str, homePos: tuple):
    parse = Parser(filename, homePos)
    parse.parse_gcode()
    parse.defCmds()

    position = posHandler(parse.positions,parse.shortendCmds,arm1,arm2)
    position.calcAngles()
    position.stepsList.insert(0,(0,0))
    servoLst = position.servoList
    print(position.stepsList)
    

    for tup in position.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])
    
def run():
    for i in range(len(stps1)):
        servo.servoMove(servoLst[i])
        motors.goTo(int(stps1[i]),int(stps2[i]), delay)
        print("Motor Positions: (" + str(motors.Pos1) + ", " + str(motors.Pos2) +" )")
        time.sleep(1)

if __name__=="__main__":
    setUp('example.gcode',homePos)
    run()