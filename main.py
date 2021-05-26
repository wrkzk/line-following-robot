# Import required libraries and modules
import check_obstacles, motor_control, os, config, numpy, turns, text_read
import eyw2_ir_sense as ir
from adafruit_motorkit import MotorKit

# Initialize the MotorKit object and calibrate the ir sensor
kit = MotorKit()
ir.calibrate()

# Find the line after calibrating
motor_control.ccw()
while True:
    current_ir = ir.read()
    if current_ir[0] == 1 or current_ir[1] == 1 or current_ir[2] == 1:
         break

# Define variables used for flow control
keep_going = True
motor_stopped = False
navigate_continue = True

# Define variables used for keeping track of the next movement
movements = text_read.read_file()
movements_pos = 0
if config.DEBUG == 1:
    print(movements)

# Navigate function to be called on every loop
def navigate():
    global movements_pos

    # Get the current ir sensor reading
    current_ir = ir.read()
    ir_avg = [numpy.mean(ir.a_vals_list[0]), numpy.mean(ir.a_vals_list[1]), numpy.mean(ir.a_vals_list[2])]
    
    if config.DEBUG == 1:
        print(current_ir)

    # If the robot is directly in front of the line, go forward
    if current_ir == [0, 1, 0]:
        motor_control.forward()

    # if the robot is veering to the left, go right
    elif current_ir == [0, 0, 1]:
        motor_control.right()

    # If the robot is veering to the right, go left
    elif current_ir == [1, 0, 0]:
        motor_control.left()
    
    # If the robot does not detect the line, go forward (this is needed to keep it going)
    elif current_ir == [0, 0, 0]:
        motor_control.forward()

    # If more than one sensor is triggered, a node has been reached
    elif current_ir == [1, 1, 1] or current_ir == [0, 1, 1] or current_ir == [1, 1, 0] or current_ir == [1, 0, 1]:
        motor_control.stop()
        os.system("espeak -a 500 'Node detected' &")
        
        if config.DEBUG == 1:
            print(movements[movements_pos])

        # If the robot has finished the defined movements, terminate the code
        if movements_pos == len(movements):
            keep_going = False

        # If the next movement is R, turn the robot to the right
        if movements[movements_pos] == "R":
            print('right')
            turns.turn_right()

        # If the next movement is L, turn the robot to the left
        elif movements[movements_pos] == "L":
            print('left')
            turns.turn_left()

        # If the next movement is TA, turn the robot around
        elif movements[movements_pos] == "TA":
            print('around')
            turns.turn_around()

        # If the next movement is S, ignore the node
        elif movements[movements_pos] == "S":
            print('straight')
            turns.straight()

        # Increment the movement by one
        movements_pos += 1

# Main loop
try:
    while keep_going:

        # Run the main navigate function
        if navigate_continue == True:
            navigate()
        
        # Check to be sure if the path in front of the robot is clear
        is_path_clear = check_obstacles.is_path_clear(30)
        
        # If the path is not clear, and the motors are not stopped, stop the motors
        if not is_path_clear and motor_stopped == False:
            if config.DEBUG == 1:
                print('Stopping...')
            os.system("espeak -a 500 'Obstacle detected. Stopping.' &")
            motor_control.stop()
            motor_stopped = True
            navigate_continue = False
    

        # If the path is clear, and the motors are stopped, start the motors up again
        elif is_path_clear and motor_stopped == True:
            if config.DEBUG == 1:
                print('Moving forward...')
            motor_control.forward()
            motor_stopped = False
            navigate_continue = True

# If the keyboard interrupt, CTRL-C, is pressed, terminate the program
except KeyboardInterrupt:
    os.system("espeak -a 500 'Keyboard interrupt detected. Stopping.' &")
    keep_going = False
       
# If the program encounters an IO Error, print a helpful message out and do not terminate the program
except IOError:
    print("An Input/Output error occured. Program still running")
  
# Stop the motors at the end of the program
motor_control.stop()
