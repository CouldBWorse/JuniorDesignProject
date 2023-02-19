import RPi.GPIO as GPIO
import time


class dualMotor:
    def __init__(self, Stp1: int, Dir1: int, Stp2: int, Dir2: int, delay1: float, delay2: float):
        self.Stp1 = Stp1
        self.Dir1 = Dir1
        self.Stp2 = Stp2
        self.Dir2 = Dir2
        self.Pos1 = 0
        self.Pos2 = 0
        self.delay1 = delay1
        self.delay2 = delay2
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Stp1, GPIO.OUT)
        GPIO.setup(Dir1, GPIO.OUT)
        GPIO.setup(Stp2, GPIO.OUT)
        GPIO.setup(Dir2, GPIO.OUT)
    
    def pulse(self,pin, delay,multiple: int):
        for i in range(multiple):
            GPIO.output(pin,1)
            time.sleep(delay/2)
            GPIO.output(pin,0)
            time.sleep(delay/2)
        
    
    def incMove(self, steps1: int, steps2: int):
        """
        Increments step position. Inputs are steps as an integer and delay in seconds.
        Outputs current position to screen after each movement.
        """
        i = 0
        ratio = max(steps1,steps2)//min(steps1,steps2)
        
        if steps1>steps2:
            maxpin = self.Stp1
            maxdelay = self.delay1
            minpin = self.Stp2
            mindelay = self.delay2
        else:
            maxpin = self.Stp2
            maxdelay = self.delay2
            minpin = self.Stp1
            mindelay = self.delay1
        #Sends pulse for total number of steps
        while i < max(steps1,steps2):
            #Determines direction based on step polarity. Sets dir pin.
            if steps1 < 0:
                GPIO.output(self.Dir1,1)
                self.Pos1 = (self.Pos1 - 1)%200
            elif steps1 >0:
                GPIO.output(self.Dir1,0)
                self.Pos1 = (self.Pos1 + 1)%200
            if steps2 < 0:
                GPIO.output(self.Dir2,1)
                self.Pos2 = (self.Pos2 - 1)%200
            elif steps2 >0:
                GPIO.output(self.Dir2,0)
                self.Pos2 = (self.Pos2 + 1)%200
            #Sending pulse to stp pin
            self.pulse(maxpin, maxdelay, ratio)
            self.pulse(minpin, maxdelay, 1)
        print(self.Pos)