from gpiozero import Servo
from time import sleep



class Setup:
    def __init__(self, pin, correction) -> None:
        
        self.servo_pin = pin  # change this to the GPIO pin your servo is connected to
        self.myCorrection = correction
        self.maxPw = (2.0 + self.myCorrection)/1000
        self.minPw = (1.0 - self.myCorrection)/1000

        servo = Servo(self.servo_pin, min_pulse_width = self.minPw, max_pulse_width = self.maxPw)


    def servoMove(self,servoPos):
        servo.value(servoPos)
