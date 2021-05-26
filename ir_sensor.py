# Import the required libraries
import eyw2_ir_sense as ir

# Calibrate the infrared sensor
ir.calibrate()

# Wrapper function that is kind of useless
def read_ir():
    ir_array = ir.read()
    return ir_array

if __name__ == "__main__":
    while True:
        ir_array = read_ir()
        print("Left sensor: {}, Center sensor: {}, Right sensor: {}".format(ir_array[0], ir_array[1], ir_array[2]))
