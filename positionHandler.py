import math
from GcodeParser import Parser


class InvalidPosition(Exception):
    """
    Raised when the gcode gives an invalid location.
    """
    pass

class posHandler:
    def __init__(self,positons: list, commands: list, arm1: int, arm2:int):
        self.positions = positons
        self.commands = commands
        self.r = arm1
        self.l = arm2
        self.angleList = []
        self.stepsList = []
    

    def calcAngles(self):
        """
        This method take the parsed G-code list of positions and turns them into a list of Angles.
        It then turns the list of angles into a list of steps.
        """
        for i in range(len(self.positions)):
            try:
                nextPos = self.positions[i]
                h=nextPos[0]
                k=nextPos[1]
                r = self.r
                l = self.l
                c = math.sqrt(h**2+k**2)

                a = ((k*math.sqrt(-r**4+2*(h**2+k**2+l**2)*r**2-h**4-2*h**2*(k**2-l**2)-k**4+2*k**2*l**2-l**4)+h*(r**2+h**2+k**2-l**2))/(2*(h**2+k**2)))
                b = (-(h*math.sqrt(-r**4+2*(h**2+k**2+l**2)*r**2-h**4-2*h**2*(k**2-l**2)-k**4+2*k**2*l**2-l**4)-k*(r**2+h**2+k**2-l**2))/(2*(h**2+k**2)))
                
                u = math.degrees(math.atan(b/a))
                v = 180-math.degrees(math.acos((l**2+r**2-c**2)/(2*l*r)))

                
                if u == -0:
                    u = 0

                self.angleList.append((u,v))

                u = round(u / 1.8,0)
                v = round(v / 1.8,0)
                self.stepsList.append((u,v))
            except ValueError:
                print(i)
                raise InvalidPosition()

#Example of how the class works
if __name__ == "__main__":
    parse = Parser('example2.gcode',(374,0,0))
    parse.parse_gcode()
    parse.defCmds()

    example = posHandler(parse.positions,parse.shortendCmds,174,200)
    example.calcAngles()
    print(example.stepsList)
