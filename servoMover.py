from gpiozero import Servo
from time import sleep

servo_pin = 18  # change this to the GPIO pin your servo is connected to

# Create a servo object
servo = Servo(servo_pin)

# Function to move the servo to a list of positions
def move_servo(positions):
    for pos in positions:
        servo.value = pos
        sleep(1)

# Example list of positions
positions = [-1, -0.5, 0, 0.5, 1]

# Move the servo to each position in turn
move_servo(positions)

# Stop the servo and clean up the GPIO pins
servo.close()