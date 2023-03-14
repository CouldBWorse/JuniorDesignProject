from gpiozero import Servo
from time import sleep

servo_pin = 22
servo = Servo(servo_pin)
def move_servo(positions):
    for pos in positions:
        servo.value = pos
        print(pos)
        sleep(0.5)

positions = [1,0.5,0,0.5,-1]

move_servo(positions)
servo.close()