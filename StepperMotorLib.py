import RPi.GPIO as GPIO
import time


class StepperMotor:
    def __init__(self, Stp, Dir, delay):
        self.Stp = Stp
        self.Dir = Dir
        self.Pos = 0
        self.delay = delay
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Stp, GPIO.OUT)
        GPIO.setup(Dir, GPIO.OUT)
        
    def incrementMove(self, steps:int):
        """
        Increments step position. Inputs are steps as an integer and delay in seconds.
        Outputs current position to screen after each movement.
        """
        time.sleep(self.delay*10)
        #Sends pulse for total number of steps
        for i in range(abs(steps)):
            #Determines direction based on step polarity. Sets dir pin.
            if steps < 0:
                GPIO.output(self.Dir,1)
                self.Pos = (self.Pos - 1)%200
            else:
                GPIO.output(self.Dir,0)
                self.Pos = (self.Pos + 1)%200
            #Sending pulse to stp pin
            GPIO.output(self.Stp,1)
            time.sleep(self.delay/2)
            GPIO.output(self.Stp,0)
            time.sleep(self.delay/2)
        print(self.Pos)

    def goTo(self, angleStp: int, delay: float):
        """
        Takes an angle as an input and moves the motor to that angle.
        """
        if angleStp > self.Pos:
            self.incrementMove(angleStp-self.Pos)
        elif angleStp < self.Pos:
            self.incrementMove(angleStp-self.Pos)
        

            
            
        
        
    


