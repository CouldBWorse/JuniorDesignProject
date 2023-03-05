#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

# declaring GPIO PINS for joystick and pen toggle
# below is a link with the GPIO pins I used as a reference
# https://www.etechnophiles.com/wp-content/uploads/2021/01/R-Pi-4-GPIO-Pinout-1-768x572.jpg?ezimgfmt=ng:webp/ngcb40
JOYSTICK_LEFT = 16
JOYSTICK_RIGHT = 20
JOYSTICK_UP = 21
JOYSTICK_DOWN = 26
PEN_TOGGLE = 27


if __name__ == '__main__':
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
                print("Here is were you would put the move left function")
                left_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            left_pressed = False
        time.sleep(0.1) # this line checks every 100 milliseconds
        
        # RIGHT DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_RIGHT):
            if not right_pressed:
                print("Here is were you would put the move right function")
                right_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            right_pressed = False
        time.sleep(0.1) # this line checks every 100 milliseconds
        
        # DOWN DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_DOWN):
            if not down_pressed:
                print("Here is were you would put the move down function")
                down_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            down_pressed = False
        time.sleep(0.1) # this line checks every 100 milliseconds
        
        # UP DIRECTION
        
        # button starts low, and when pulled to high it prints or eventually will run the function to move the arm
        if GPIO.input(JOYSTICK_UP):
            if not up_pressed:
                print("Here is were you would put the move up function")
                up_pressed = True
        # when the joystick is not being depressed it returns the button state to false
        else:
            up_pressed = False
        time.sleep(0.1) # this line checks every 100 milliseconds
        
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
                pen_up = True
        
        if not GPIO.input(PEN_TOGGLE):
            if pen_up:
                print("switching pen to down")
                pen_up = False
        time.sleep(0.1)