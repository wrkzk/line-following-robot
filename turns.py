# Import required libraries
import motor_control, time, config
import eyw2_ir_sense as ir

# Turn right until the line is under the sensor, at which point start moving forward again
def turn_right():
    motor_control.forward()
    time.sleep(1)
    motor_control.stop()
    
    motor_control.cw()
    time.sleep(0.8)

    while True:
        current_ir = ir.read()
        if current_ir[0] == 1 or current_ir[1] == 1 or current_ir[2] == 1:
            print('right turn line found')
            return

# Turn left until the correct line is under the sensor, at which point start moving forward again
def turn_left():
    motor_control.forward()
    time.sleep(1)
    motor_control.stop()
    
    motor_control.ccw()
    time.sleep(0.8)

    while True:
        current_ir = ir.read()
        if current_ir[0] == 1 or current_ir[1] == 1 or current_ir[2] == 1:
            return

# Turn around until the correct line is under the sensor, at which point start moving forward again
def turn_around():
    motor_control.forward()
    time.sleep(1.75)
    motor_control.cw()
    time.sleep(1.3)

    while True:
        current_ir = ir.read()
        if current_ir[0] == 1 or current_ir[1] == 1 or current_ir[2] == 1:
            return

# Move forward, ignoring the node
def straight():
    motor_control.forward()
    time.sleep(0.2)

if __name__ == '__main__':
    #ir.calibrate()
    #correct_right()
    #correct_left()
    #print(correct_back())
    turn_around()
