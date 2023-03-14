#!/usr/bin/env python3
import math
import time
import RPi.GPIO as GPIO
from dualStepperMotor import dualMotor
from gpiozero import Servo

# declaring GPIO PINS for joystick and pen toggle
# below is a link with the GPIO pins I used as a reference
# https://www.etechnophiles.com/wp-content/uploads/2021/01/R-Pi-4-GPIO-Pinout-1-768x572.jpg?ezimgfmt=ng:webp/ngcb40
JOYSTICK_LEFT = 16
JOYSTICK_RIGHT = 20
JOYSTICK_UP = 21
JOYSTICK_DOWN = 26
PEN_TOGGLE = 19
curLoc = (374,0,1)##mm
armLength = (174,200)##mm
inc = 50 ##mm
delay = 0.03 ##seconds
servo_pin = 13


servo = Servo(servo_pin)
motors = dualMotor(6, 5, 9, 11)

def calcAngles(h,k):
        """
        This method take the parsed G-code list of positions and turns them into a list of Angles.
        It then turns the list of angles into a list of steps.
        """
    
        try:
            r = armLength[0]
            l = armLength[1]
            c = math.sqrt(h**2+k**2)

            a = ((k*math.sqrt(-r**4+2*(h**2+k**2+l**2)*r**2-h**4-2*h**2*(k**2-l**2)-k**4+2*k**2*l**2-l**4)+h*(r**2+h**2+k**2-l**2))/(2*(h**2+k**2)))
            b = (-(h*math.sqrt(-r**4+2*(h**2+k**2+l**2)*r**2-h**4-2*h**2*(k**2-l**2)-k**4+2*k**2*l**2-l**4)-k*(r**2+h**2+k**2-l**2))/(2*(h**2+k**2)))
            
            u = math.degrees(math.atan(b/a))
            v = 180-math.degrees(math.acos((l**2+r**2-c**2)/(2*l*r)))

            
            if u == -0:
                u = 0

            u = int(round(u / 1.8,0))
            v = int(round(v / 1.8,0))
            newLoc = (u,v)
            return newLoc
        except ValueError:
            print("Invalid Position")
            


def analogControl():
    # setting up the state of the GPIO pins used for the while loop
    # starting them all in the low position since we are using a pull down resistor config
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(JOYSTICK_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(JOYSTICK_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(JOYSTICK_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(JOYSTICK_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PEN_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # initial state for the joystick will be all false
    # initial state for the pen toggle switch will be up, we can reverse it and change it to down if we need to
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False
    pen_up = True

    while True:
        # LEFT DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_LEFT):
            if not left_pressed:
                print("Moving Left")
                stps = calcAngles(curLoc[0] - inc, curLoc[1])
                motors.goTo(stps[0],stps[1], delay)
                curLoc = (curLoc[0] - inc, curLoc[1])
                print(curLoc)
                left_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            left_pressed = False
        
        
        # RIGHT DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_RIGHT):
            if not right_pressed:
                print("Moving Right")
                stps = calcAngles(curLoc[0] + inc, curLoc[1])
                motors.goTo(stps[0],stps[1], delay)
                curLoc = (curLoc[0] + inc, curLoc[1])
                print(curLoc)
                right_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            right_pressed = False
        
        
        # DOWN DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_DOWN):
            if not down_pressed:
                print("Moving Down")
                stps = calcAngles(curLoc[0], curLoc[1] - inc)
                motors.goTo(stps[0],stps[1], delay)
                curLoc = (curLoc[0], curLoc[1] - inc)
                print(curLoc)
                down_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            down_pressed = False
        
        
        # UP DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_UP):
            if not up_pressed:
                print("Moving Up")
                stps = calcAngles(curLoc[0], curLoc[1]+inc)
                motors.goTo(stps[0],stps[1], delay)
                curLoc = (curLoc[0], curLoc[1]+inc)
                print(curLoc)
                up_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            up_pressed = False
        
        
        # PEN TOGGLE
        
        # The toggle starts high ( up position) and can be toggled to down
        #if not GPIO.input(PEN_TOGGLE) and pen_up == True:
            #print("Here is where you would put the move pen up function")
            #pen_up = False
        #if GPIO.input(PEN_TOGGLE) and pen_up == False:
            #print("Here is where you would put the move pen down function")
            #pen_up = True
        
        if GPIO.input(PEN_TOGGLE):
            if not pen_up:
                print("switching pen to up")
                servo.value = 1
                pen_up = True
        
        if not GPIO.input(PEN_TOGGLE):
            if pen_up:
                print("switching pen to down")
                servo.value = 0
                pen_up = False
        time.sleep(0.1)
