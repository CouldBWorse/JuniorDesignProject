from gpiozero import Servo
from time import sleep



class Setup:
    def __init__(self, pin, correction) -> None:
        
        self.servo_pin = pin  # change this to the GPIO pin your servo is connected to
        #self.myCorrection = correction
        #self.maxPw = (2.0 + self.myCorrection)/1000
        #self.minPw = (1.0 - self.myCorrection)/1000

        servo = Servo(pin)


    def servoMove(self,servoPos):
        servo.value = servoPos
        


if __name__ == "__main__":
    servo = Setup(22,0)
    servo.servoMove(1)
    sleep(0.5)
    servo.servoMove(-1)
    
    


#, min_pulse_width = self.minPw, max_pulse_width = self.maxPw