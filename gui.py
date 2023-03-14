"""Will create a GUI to be integrated with the rest of the code."""
from GcodeParser import Parser
from positionHandler import posHandler
from dualStepperMotor import dualMotor
from gpiozero import Servo
import RPi.GPIO as GPIO
import time
import math
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

motors = dualMotor(6, 5, 9, 11)
arm1 = 174
arm2 = 200
homePos = (arm1 + arm2,0,0)
stps1 = []
stps2 = []
servoLst = []
delay = 0.02
inc = 50 ##mm
curLoc = (374,0,0)##mm
armLength = (174,200)
cmds = []


servo_pin = 13
servo = Servo(servo_pin)

JOYSTICK_LEFT = 16
JOYSTICK_RIGHT = 20
JOYSTICK_UP = 21
JOYSTICK_DOWN = 26
PEN_TOGGLE = 19

def setUp(filename: str, homePos: tuple):
    exampleParse = Parser(filename, homePos)
    exampleParse.parse_gcode()
    exampleParse.defCmds()

    example = posHandler(exampleParse.positions,exampleParse.shortendCmds,arm1,arm2)
    example.calcAngles()
    example.stepsList.insert(0,(0,0))
    example.servoList.insert(0,1)


    for i in range(len(example.servoList)):
        servoLst.append(example.servoList[i])
        
    for i in range(len(exampleParse.shortendCmds)):
        cmds.append(exampleParse.shortendCmds[i])
    
    for tup in example.stepsList:
        stps1.append(tup[0])
        stps2.append(tup[1])
        
    print(example.stepsList)
    print(servoLst)

def run():
    for i in range(len(stps1)):
        servo.value = servoLst[i]
        time.sleep(1)
        motors.goTo(int(stps1[i]),int(stps2[i]), delay)
        print("Motor Positions: (" + str(motors.Pos1) + ", " + str(motors.Pos2) +" )")
        if cmds[i-1] == 'M6':
            toolChange = input("Press keyboard to continue")
        time.sleep(1)
        
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
            
def analogControl(curLoc):
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
    try:
        while True:
            # LEFT DIRECTION
            try:
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
            except:
                print("Invalid Position")
                time.sleep(2)
    except KeyboardInterrupt:
        print("Exit Analog Mode")
        curLoc = (374,0,1)
        return






def gcode_pressed():
    """Change the text on the screen to say G-code Mode."""
    lbl_value.config(text="G-code Mode \nEnter file name below:")
    inputfile.grid(row=1, column=1, sticky="nsew")
    btn_run_file.grid(row=2, column=1, sticky="nsew")
    btn_ten_inch.grid(row=2, column=0, sticky="nsew")
    btn_speed_test.grid(row=2, column=2, sticky="nsew")
    return


def analog_pressed():
    """Change the text on the screen to say G-code Mode."""
    lbl_value.config(text="Analog Mode")
    inputfile.grid_forget()
    btn_run_file.grid_forget()
    btn_speed_test.grid_forget()
    btn_ten_inch.grid_forget()
    analogControl(curLoc)
    return


def run_gcode():
    """Fill in the rest of the code with your functions to run the gcode."""
    file_name = inputfile.get(1.0,'end-1c')
    try:
        setUp(file_name,homePos)
        run()
    except:
        print("Invalid Filename")
    return

def ten_inch_line():
    """Ten inch line function goes here."""
    print("Align Arm at 45 degrees from the X-Axis.")
    waitingInput1 = input("Press enter to draw line")
    servo.value = 0
    motors.goTo(-38,76,0.015)
    return


def speed_test():
    """Speed test function goes here."""
    print("Align Arm on the X-Axis and set up ruler/stopwatch.")
    waitingInput2 = input("Press enter to draw line")
    motors.goTo(-40,80,0.015)
    return

font_variable = "Helvetica, 20"
window = tk.Tk()
window.title("Robotic Arm Interface")
lbl_value = tk.Label(master=window, font=font_variable, text="Select a mode")
lbl_value.grid(row=0, column=1)
window.rowconfigure([0, 1, 2], minsize=200, weight=1)
window.columnconfigure([0, 1, 2], minsize=200, weight=1)
btn_gcode_mode = tk.Button(master=window, font=font_variable, text="G-code Mode",
                           command=gcode_pressed,)
btn_gcode_mode.grid(row=0, column=0, sticky="nsew")

btn_analog_mode = tk.Button(master=window, font=font_variable, text="Analog Mode",
                            command=analog_pressed)
btn_analog_mode.grid(row=0, column=2, sticky="nsew")

inputfile = tk.Text(window, font=font_variable, height=10, width=10)

btn_run_file = tk.Button(window, font=font_variable, text="Click here to run file",
                         command=run_gcode)

btn_ten_inch = tk.Button(window, font=font_variable, text="10 inch line", command=ten_inch_line)

btn_speed_test = tk.Button(window, font=font_variable, text="Speed test", command=speed_test)

window.mainloop()