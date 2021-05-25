import check_obstacles, motor_control, os, config, numpy, turns, text_read
import eyw2_ir_sense as ir
from adafruit_motorkit import MotorKit

kit = MotorKit()
ir.calibrate()

keep_going = True
motor_stopped = False
navigate_continue = True

movements = text_read.read_file()
movements_pos = 0
print(movements)

def find_line():
    turns.correct_back()
    #left_average = numpy.mean(ir.a_vals_list[0])
    #right_average = numpy.mean(ir.a_vals_list[2])
    #if left_average > right_average:
    #    return turns.correct('left')    
    #elif right_average > left_average:    
    #    return turns.correct('right')
        
def navigate():
    global movements_pos

    current_ir = ir.read()
    ir_avg = [numpy.mean(ir.a_vals_list[0]), numpy.mean(ir.a_vals_list[1]), numpy.mean(ir.a_vals_list[2])]
    #print(ir_avg)
    
    if config.DEBUG == 1:
        print(current_ir)

    if current_ir == [0, 1, 0]:
        motor_control.forward()

    #elif current_ir == [0, 1, 1]:
    #    motor_control.right()

    elif current_ir == [0, 0, 1]:
        motor_control.right()

    #elif current_ir == [1, 1, 0]:
    #    motor_control.left()

    elif current_ir == [1, 0, 0]:
        motor_control.left()
    
    elif current_ir == [0, 0, 0]:
        #if ir_avg[0] <= 20 and ir_avg[1] <= 20 and ir_avg[2] <= 20:            
        #    print('Line lost')        
        #    find_line()        
        #else:
        
        #print('No line, moving forward')
        motor_control.forward()

    elif current_ir == [1, 1, 1] or current_ir == [0, 1, 1] or current_ir == [1, 1, 0] or current_ir == [1, 0, 1]:
        motor_control.stop()
        os.system("espeak -a 500 'Node detected' &")
        print(movements[movements_pos])

        if movements[movements_pos] == "R":
            print('right')
            turns.turn_right()

        elif movements[movements_pos] == "L":
            print('left')
            turns.turn_left()

        elif movements[movements_pos] == "TA":
            print('around')
            turns.turn_around()

        elif movements[movements_pos] == "S":
            print('straight')
            turns.straight()

        movements_pos += 1

try:
    while keep_going:
        if navigate_continue == True:
            navigate()

        is_path_clear = check_obstacles.is_path_clear(30)

        if not is_path_clear and motor_stopped == False:
            if config.DEBUG == 1:
                print('Stopping...')
            os.system("espeak -a 500 'Obstacle detected. Stopping.' &")
            motor_control.stop()
            motor_stopped = True
            navigate_continue = False

        elif is_path_clear and motor_stopped == True:
            if config.DEBUG == 1:
                print('Moving forward...')
            motor_control.forward()
            motor_stopped = False
            navigate_continue = True

except KeyboardInterrupt:
    os.system("espeak -a 500 'Keyboard interrupt detected. Stopping.' &")
    keep_going = False
       
except IOError:
    print("An Input/Output error occured. Program still running")
        
motor_control.stop()
