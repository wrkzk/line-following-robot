from adafruit_motorkit import MotorKit
import config
kit = MotorKit()
import time

def forward():
    kit.motor1.throttle = 0.28
    kit.motor2.throttle = 0.28
    
def backward():
    kit.motor1.throttle = -0.28
    kit.motor2.throttle = -0.28
    
def left():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0.265
    
def right():
    kit.motor1.throttle = 0.265
    kit.motor2.throttle = 0
    
def cw():
    kit.motor1.throttle = 0.30
    kit.motor2.throttle = -0.30
        
def ccw():
    kit.motor1.throttle = -0.30
    kit.motor2.throttle = 0.30

def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
if __name__ == "__main__":
    forward()
