# Import the required libraries
import mechatronics as mech
import os, config

# Define variables for the ultrasonic sensor pins
trig_one = 24
echo_one = 8

trig_two = 23
echo_two = 7

# Initialize the range sensors
mech.initialize_ranger(trig_one, echo_one)
mech.initialize_ranger(trig_two, echo_two)

# Set up arrays to calculate the rolling average
d_one = [100, 100]
d_two = [100, 100]

# Function to check if the path is clear
def is_path_clear(safe_distance):

    # Get the two current distances
    cd_one = mech.get_distance(trig_one, echo_one)
    cd_two = mech.get_distance(trig_two, echo_two)
    
    # Append the distances to the arrays
    if cd_one == None:
        cd_one = d_one[1]
    del d_one[0]
    d_one.append(cd_one)
    
    if cd_two == None:
        cd_two = d_two[1]
    del d_two[0]
    d_two.append(cd_two)

    # Calculate the average of the arrays
    d_one_avg = (d_one[0] + d_two[1]) / 2
    d_two_avg = (d_two[0] + d_two[1]) / 2

    # Return False if the average of either sensor is below the safe distance
    if d_one_avg < safe_distance or d_two_avg < safe_distance:
        if config.DEBUG == 1:
            print(str(d_one_avg), str(d_two_avg))
            return False

    # Otherwise, return True
    return True

if __name__ == "__main__":
    while True:
        print(mech.get_distance(trig_two, echo_two))
