import RPi.GPIO as GPIO
import time


class dualMotor:
    def __init__(self, Stp1: int, Dir1: int, Stp2: int, Dir2: int):
        self.Stp1 = Stp1
        self.Dir1 = Dir1
        self.Stp2 = Stp2
        self.Dir2 = Dir2
        self.Pos1 = 0
        self.Pos2 = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Stp1, GPIO.OUT)
        GPIO.setup(Dir1, GPIO.OUT)
        GPIO.setup(Stp2, GPIO.OUT)
        GPIO.setup(Dir2, GPIO.OUT)
    
    def pulse(self,pin: int, delay: float):
        GPIO.output(pin,1)
        time.sleep(delay/2)
        GPIO.output(pin,0)
        time.sleep(delay/2)
        
    
    def incMove(self, steps1: int, steps2: int, delay: float):
        """
        Increments step position. Inputs are steps as an integer and delay in seconds.
        Outputs current position to screen after each movement.
        """
        Dif1 = abs(steps1)%200
        Dif2 = abs(steps2)%200
        
        if steps1 < 0 and self.Pos1 + steps1 < 0:
            limit1 = 200+(self.Pos1 + steps1)
        elif self.Pos1 + steps1 > 200:
            limit1 = (self.Pos1 + steps1)-200
        else:
            limit1 = self.Pos1 + steps1
        
        if steps2 < 0 and self.Pos2 + steps2 < 0:
                    200-(self.Pos2 + steps2)
        else:
            limit2 = self.Pos2 + steps2
        
        for i in range(max(abs(steps1),abs(steps2))):
            #Determines direction based on step polarity. Sets dir pin.
            #print("Pos1: " + str(motors.Pos1))
            #print("Pos2: " + str(motors.Pos2))
            if steps1 < 0:
                GPIO.output(self.Dir1,1)
                direction1 = -1
                
            elif steps1 > 0:
                GPIO.output(self.Dir1,0)
                direction1 = 1
            
            if steps2 < 0:
                GPIO.output(self.Dir2,1)
                direction2 = -1
                
            elif steps2 > 0:
                GPIO.output(self.Dir2,0)
                direction2 = 1                
            
            
            if Dif1 > Dif2:
                self.pulse(self.Stp1,0.01)
                self.Pos1 = (self.Pos1 + direction1)%200
                                   
                    
                if (i % (Dif1//Dif2)) == 0 and self.Pos2 != limit2:
                    #print(self.Pos2)
                    self.pulse(self.Stp2,delay)
                    self.Pos2 = (self.Pos2 + direction2)%200
                    
            elif Dif1 < Dif2:
                self.pulse(self.Stp2,delay)
                self.Pos2 = (self.Pos2 + direction2)%200
                    
                    
                if (i % (Dif2//Dif1)) == 0 and self.Pos1 != limit1:
                    self.pulse(self.Stp1,0.01)
                    self.Pos1 = (self.Pos1 + direction1)%200
            else:
                self.pulse(self.Stp1,delay)
                self.pulse(self.Stp2,delay)
          
                  

    def goTo(self, loc1: int, loc2: int, delay: float):
        """
        Takes two steps as an input and moves the motors to their respective steps.
        """
        if self.Pos1 > 100 and self.Pos2 > 100:
            dif1 = (200 - self.Pos1) + loc1
            dif2 = (200 - self.Pos2) + loc2
        elif self.Pos1 > 100:
            dif1 = (200 - self.Pos1) + loc1
            dif2 = loc2-self.Pos2
        elif self.Pos2 > 100:
            dif1 = loc1-self.Pos1
            dif2 = (200 - self.Pos2) + loc2
        else:
            dif1 = loc1-self.Pos1
            dif2 = loc2-self.Pos2
        
        self.incMove(dif1, dif2, delay)
        







if __name__ == "__main__":
    motors = dualMotor(6, 5, 9, 11)
    motors.goTo(0,0,0.02)
    print(motors.Pos1)
    print(motors.Pos2)
    time.sleep(1)
    motors.goTo(-38,76,0.01)
    print(motors.Pos1)
    print(motors.Pos2)
    time.sleep(1)
    
    
    