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
        
    def incMove(self, steps:int):
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
            time.sleep((self.delay)/2)
            GPIO.output(self.Stp,0)
            time.sleep((self.delay)/2)
        print(self.Pos)

    def goTo(self, angleStp: int):
        """
        Takes an angle as an input and moves the motor to that angle.
        """
        if self.Pos > 100:
            self.incMove((200-self.Pos)+angleStp)
        elif angleStp > self.Pos:
            self.incMove(angleStp-self.Pos)
        elif angleStp < self.Pos:
            self.incMove(angleStp-self.Pos)

#Example of how the class works
if __name__ == "__main__":
    motor1 = StepperMotor(19,26,0.03)
    motor1.goTo(-10)
    motor1.goTo(50)
    motor1.goTo(0)
    motor1.goTo(25)
    motor1.goTo(-25)
    motor1.goTo(0)

        
        
    


