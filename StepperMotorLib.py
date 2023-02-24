import RPi.GPIO as GPIO
import time


class StepperMotor:
    def __init__(self, Stp, Dir):
        self.Stp = Stp
        self.Dir = Dir
        self.Pos = 0
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Stp, GPIO.OUT)
        GPIO.setup(Dir, GPIO.OUT)
        
    def incMove(self, steps:int, delay: float):
        """
        Increments step position. Inputs are steps as an integer and delay in seconds.
        Outputs current position to screen after each movement.
        """
        time.sleep(0.05)
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
            time.sleep(0.02)
            GPIO.output(self.Stp,0)
            time.sleep((delay)/2)
            


    def goTo(self, angleStp: int, delay: float):
        """
        Takes an angle as an input and moves the motor to that angle.
        """
        if self.Pos > 100:
            self.incMove((200-self.Pos)+angleStp, delay)
        elif angleStp > self.Pos:
            self.incMove(angleStp-self.Pos, delay)
        elif angleStp < self.Pos:
            self.incMove(angleStp-self.Pos, delay)

#Example of how the class works
if __name__ == "__main__":
    motor1 = StepperMotor(20,21)
    motor2 = StepperMotor(19,26)
    motor1.goTo(-40,0.02)
    motor2.goTo(75,0.02)
    motor1.goTo(20,0.02)
    motor2.goTo(20,0.02)
        
        
    


