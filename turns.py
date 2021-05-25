import motor_control, time, config
import eyw2_ir_sense as ir

def correct_right():
    motor_control.left()
    time.sleep(2)
    motor_control.stop()
    time.sleep(1)
    
    for x in range(0, config.MAX_ATTEMPTS):
        for x in range(0, 200):
            motor_control.forward()
            current_read = ir.read()
            if current_read[0] == 1 or current_read[1] == 1 or current_read[2] == 1:
                return True
                motor_control.stop()
            time.sleep(1)
    
    return False
    
def correct_left():
    motor_control.right()
    time.sleep(2)
    motor_control.stop()
    time.sleep(1)
    
    for x in range(0, config.MAX_ATTEMPTS):
        for x in range(0, 200):
            motor_control.forward()
            current_read = ir.read()
            if current_read[0] == 1 or current_read[1] == 1 or current_read[2] == 1:
                return True
                motor_control.stop()
            time.sleep(1)
            
    return False
    
def correct_back():
    motor_control.stop()
    time.sleep(1)

    for x in range(0, config.MAX_ATTEMPTS):
        for x in range(0, 200):
            motor_control.backward()
            current_read = ir.read()
            if current_read[0] == 1 or current_read[1] == 1 or current_read[2] == 1:
                return True
                motor_control.stop()
            time.sleep(1)
    
    return False
    
def turn_right():
    motor_control.forward()
    time.sleep(0.3)
    motor_control.stop()
    
    motor_control.cw(0.5)
    
def turn_left():
    motor_control.forward()
    time.sleep(0.3)
    motor_control.stop()
    
    motor_control.ccw(0.5)

def turn_around():
    motor_control.cw(1.5)

def straight():
    motor_control.forward()
    time.sleep(1)

if __name__ == '__main__':
    #ir.calibrate()
    #correct_right()
    #correct_left()
    #print(correct_back())
    turn_around()
