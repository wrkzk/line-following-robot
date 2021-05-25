"""

    EYW II Unit 5 Hospital Delivery Vehicle
    File: U05_L08_line_following_02.py (python 2.7.9)

    File: eyw_ir_sense.py (python 2.7.9)
    Follows Programming Contract 5d.
    Date: 3/30/18
    Version 4.1
    Vincent O'Sullivan
    The University of Texas at Austin, Engineer Your World
    rev_01: Contains calibration and read functions for Pololu QTR-8RC IR sensor
    array.
    rev_02: Add printing control with DEBUG variable. Access DEBUG variable by
    importing U05_L08_robot_config_01.py.
    U05_L08_ir_sense_03: Update moto to U05_L04_bot_bkwd_fwd_06, update cf to
    U05_L08_robot_config_03.py. 
    eyw_ir_sense.py: Initial version 2/16/18
    rev_03.py - 3/9/18: Removed all dependencies on student created modules such as
    05_L04_bot_bkwd_fwd_06 and U05_L08_robot_config_03.py. This file has to work
    independent of student created files.
    Available functions
    calibrate()
        Takes data from the actual line and background that the robot will follow to determine
        the value for darkest and lightes regions. These will be converted to values
        between 0 and MAX_SCALE.
        Args:
            None
        Returns:
            None
        Raises:
            None

    read():
       
        Read values from IR sensors and converts them, using calibration constants determined
        calibration() function to a scale between 0 and MAC_SCALE.
        Args:
            None
        Returns:
            d_vals_list: a three element array as follows
            [value of left sensor,value of middle sensor, value of right sensor]
            where values are 0 (for light background) or 1 (for dark backbround).
        Raises:
            None
             
    Available variables:
        a_vals_list: a three element array as follows
        [average value of last five left sensor readings, average value of last five middle sensor readings,
            average value of last five right sensor readings].
"""
import numpy
import pigpio
import time
import config
from adafruit_motorkit import MotorKit

kit = MotorKit()

# Set default motor speed 0 - 255
MOTOR_SPEED = 0.35
#Create a pi object from the pigpio library
pi = pigpio.pi()

# Use finish to signal for loop control when reading IR sensors.
finish = 0

# Max output scale for IR sensors.
OUTPUT_SCALE = 100

# Using only 3 of eight channels on the Pololu IR sense array
IR_SENS_L = 22   
IR_SENS_C = 27
IR_SENS_R = 4

# Assign value for number of channels used. This
# will be used for iterating over all the channel values.
IR_MAX_CHANNELS = 3

# Create two dimensional list that will hold sensor readback values for each
# sensor channel. The min and max readings for each channel will then be used to
# calibrate that channel.
ir_cal_rdgs = [[], [], []]

# Create lists for each of the elements in the cal_rdgs list.
ir_chan_list = [IR_SENS_L, IR_SENS_C, IR_SENS_R]
ir_m_list = [0,0,0]
ir_b_list = [0,0,0]

# Create list that will contain either 1's or 0's depending
# on the value sensed by each of the 3 IR channels used. 
# Must adjust depending on number of channels used.
d_vals_list = [0,0,0]

# The following two dimensional list will contain the last five analog readings of
# the 3 IR channels used. Values will range between 0 and OUTPUT_SCALE.
# This list will be used to determine if robot has veered left or
# right after losing line.
a_vals_list =[[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]

# CAL_PASSES is the number of IR sensors readings taken to perform
# calibration

CAL_PASSES = 8000

# Speed of motors during calibration.
#kit.motor1.throttle = MOTOR_SPEED
#kit.motor2.throttle = MOTOR_SPEED

#Local DEBUG variable. Valid in this file only.

DEBUG = 0 
# ******************************* Function Definitions *****************************


def calibrate():
    """ 
    Takes data from the actual line and background that the robot will follow to determine
    the value for darkest and lightes regions. These will be converted to values
    between 0 and MAX_SCALE.
    Args:
        None
    Returns:
        None
    Raises:
        None
         
    """
    kit.motor1.throttle = config.CALIBRATE_SPEED
    kit.motor2.throttle = -config.CALIBRATE_SPEED
    if DEBUG == 1: print("Clockwise")

    for n in range(CAL_PASSES):
        if n == CAL_PASSES/2:
            kit.motor1.throttle = -config.CALIBRATE_SPEED
            kit.motor2.throttle = config.CALIBRATE_SPEED
            if DEBUG == 1: print("Counter Clockwise")
        for i  in range(IR_MAX_CHANNELS):
            # The following code sets a GPIO to output, drives a high, waits
            # 10 microseconds, then changes the GPIO channel to an input making sure
            # there is no pull up or pull down that would prematurely bleed off charge.
            # The time it takes for the channel to go low is measured. This time is inversely
            # proportional to the amount of IR impingent on the sensor.
            # Black lines will have a long delay ~ 3 milliseconds, light surfaces will have a short
            # delay ~ 10 microseconds.
            finish = 0
            pi.set_mode(ir_chan_list[i],pigpio.OUTPUT)
            pi.write(ir_chan_list[i], 1)
            time.sleep(.00001)
            pi.set_mode(ir_chan_list[i],pigpio.INPUT)
            pi.set_pull_up_down(ir_chan_list[i],pigpio.PUD_OFF)
            start = time.time()
            while pi.read(ir_chan_list[i]) == 1:
                finish = time.time()
            delay = finish - start
            #print(delay, n)
            # On light backgrounds the above loop may not be entered due to
            # the rapid decay of the "high" signal.
            # This results in a negative min value which will throw
            # off the interpolation. IN this case set, delay to 0. 
            if delay < 0:
                delay = 0
            ir_cal_rdgs[i].append(delay)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    if DEBUG == 1: print("Halt")
    
    for i in range(IR_MAX_CHANNELS):
        max_val = max(ir_cal_rdgs[i])   
        min_val = min(ir_cal_rdgs[i])
        if DEBUG == 1: print  ("max = ", max_val)
        if DEBUG == 1: print  ("min = ", min_val)
        # Use the fact that, given two points of a straight line, the slope (m) and
        # y intercept (b) of the straight line can be computed. Once m and b are computed
        # any ir sensor reading (x) can be converted to a scale between 0 and OUTPUT_SCALE
        # using y = mx + b, where x is the sensor reading and y is the value between 0
        # and OUTPUT_SCALE.
        m = OUTPUT_SCALE/(max_val - min_val)
        ir_m_list[i] = m
        ir_b_list[i] = - m * min_val
        
    if DEBUG == 1: print ("Calibration complete.")

    

def read():
    """
    Read values from IR sensors and converts them, using calibration constants determined
    calibration() function to a scale between 0 and MAC_SCALE.
    Args:
        None
    Returns:
        d_vals_list: a three elementt array as follows
        [value of left sensor,value of middle sensor, value of right sensor]
        where values are 0 (for light background) or 1 (for dark backbround).
    Raises:
        None
         
    """
    for i in range(IR_MAX_CHANNELS):
        # See calibration() for sensor read method.
        sens = ir_chan_list[i]
        pi.set_mode(sens,pigpio.OUTPUT)
        pi.write(sens, 1)
        time.sleep(.00001)
        pi.set_mode(sens,pigpio.INPUT)
        pi.set_pull_up_down(sens,pigpio.PUD_OFF)
        finish = 0
        start = time.time()
        while pi.read(sens)== 1:
            finish = time.time()
        delay = finish - start
        #print(delay)
        if DEBUG == 1: print ("start", start, "finish", finish) 
        # The following line employs the slope (m) and y intercept (b)
        # calibration constants deterimed in the calibration function.
        a_val = delay * ir_m_list[i] + ir_b_list[i]
        if DEBUG == 1: print ("a_val", int(a_val),)
        # The threshold for high and low signals will vary within the range
        # of the selected output scale. 
        # a_val > 40: worked for masking tap on green vinyl
        # a_val > 20 works for electricians tape on white poster board.
        if a_val > 20:
            d_vals_list[i] = 1
        else:
            d_vals_list[i] = 0
        del a_vals_list[i][0]
        a_vals_list[i].append(a_val)
        if DEBUG == 1: print ("i d_vals_list", i, d_vals_list[i])
    return d_vals_list        

def clear_res():
    """
    Release pigpio resources.
    """

    pi.stop()

def primary():
    calibrate()
    while (True):
        array = read()
        print(array)

    clear_res()

    
# End of Function Definitions


## *********************** Start main program here.*************************
if __name__ == '__main__':
    primary()
