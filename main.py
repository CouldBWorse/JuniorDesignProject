from GcodeParser import Parser
from positionHandler import posHandler
from StepperMotorLib import StepperMotor
import time
import multiprocessing

motor2 = StepperMotor(19,26)
motor1 = StepperMotor(20,21)
arm1 = 174
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
    example.stepsList.insert(0,(0,0))
    print(example.stepsList)
    

    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])
        


def run(motorNum: int,):
    if motorNum == 1:
        for i in range(len(stps1)):
            time.sleep(1)
            intStp1 = int(stps1[i])
            intStp2 = int(stps2[i])
            
            dif1 = abs(intStp1-int(stps1[i-1]))
            dif2 = abs(intStp2-int(stps2[i-1]))
            
            if dif1 > 100:
                dif1 = 200 - dif1
            elif dif2 > 100:
                dif2 = 200 - dif2
             
            if dif2 <= dif1 or dif1 == 0:
                delay1 = 0.01
            else:
                delay1 = 0.01*abs(dif2//dif1)
                
            
            motor1.goTo(intStp1, delay1)
            print("Motor1: " + str(motor1.Pos))
    
    elif motorNum == 2:
        for i in range(len(stps2)):
            time.sleep(1)
            intStp1 = int(stps1[i])
            intStp2 = int(stps2[i])
            dif1 = abs(intStp1-int(stps1[i-1]))
            dif2 = abs(intStp2-int(stps2[i-1]))
            
            if dif1 > 100:
                dif1 = 200 - dif1
            elif dif2 > 100:
                dif2 = 200 - dif2
                
            #print("Dif1: " + str(dif1) + ", Dif2: " + str(dif2))
            
            if dif1 <= dif2 or dif2 == 0:
                delay2 = 0.01
            else:
                delay2 = 0.01*abs(dif1//dif2)
                
            
            motor2.goTo(intStp2,delay2)
            print("Motor2: " + str(motor2.Pos))

setUp('example2.gcode',homePos)

p1 = multiprocessing.Process(target=run, args=(1,))
p2 = multiprocessing.Process(target=run, args=(2,))
        
p1.start()
p2.start()
        
p1.join()
p2.join()