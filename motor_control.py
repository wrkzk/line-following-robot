from adafruit_motorkit import MotorKit
import config
kit = MotorKit()
import time

def forward():
    kit.motor1.throttle = 0.32
    kit.motor2.throttle = 0.35
    
def backward():
    kit.motor1.throttle = -0.32
    kit.motor2.throttle = -0.35
    
def left():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0.35
    
def right():
    kit.motor1.throttle = 0.35
    kit.motor2.throttle = 0
    
def cw():
    kit.motor1.throttle = 0.35
    kit.motor2.throttle = -0.35
        
def ccw():
    kit.motor1.throttle = -0.35
    kit.motor2.throttle = 0.35

def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
if __name__ == "__main__":
    forward()
