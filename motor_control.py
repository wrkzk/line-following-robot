# Import required libraries
from adafruit_motorkit import MotorKit
import config
import time

# Initialize the MotorKit object
kit = MotorKit()

# Move the robot forward
def forward():
    kit.motor1.throttle = config.NORMAL_SPEED
    kit.motor2.throttle = config.NORMAL_SPEED
    
# Move the robot backward
def backward():
    kit.motor1.throttle = -config.NORMAL_SPEED
    kit.motor2.throttle = -config.NORMAL_SPEED

# Correct the robot left
def left():
    kit.motor1.throttle = 0
    kit.motor2.throttle = config.NORMAL_SPEED

# Correct the robot right
def right():
    kit.motor1.throttle = config.NORMAL_SPEED
    kit.motor2.throttle = 0
    
# Turn the robot clockwise
def cw():
    kit.motor1.throttle = config.NORMAL_SPEED
    kit.motor2.throttle = -config.NORMAL_SPEED
        
# Turn the robot counterclockwise
def ccw():
    kit.motor1.throttle = -config.NORMAL_SPEED
    kit.motor2.throttle = config.NORMAL_SPEED

# Stop the robot
def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
if __name__ == "__main__":
    forward()
