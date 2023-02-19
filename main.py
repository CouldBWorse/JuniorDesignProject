from GcodeParser import Parser
from positionHandler import posHandler


exampleParse = Parser('example.gcode', (370,0,0))
exampleParse.parse_gcode()
exampleParse.defCmds()

example = posHandler(exampleParse.positions,exampleParse.shortendCmds,170,200)
example.calcAngles()
print(example.angleList)
motor1 = []
motor2 = []


for tup in example.stepsList:
    motor1.append(tup[0])
    motor2.append(tup[1])

print(motor1)
print(motor2)