import mechatronics as mech
import os, config

trig_one = 24
echo_one = 8

trig_two = 23
echo_two = 7

mech.initialize_ranger(trig_one, echo_one)
mech.initialize_ranger(trig_two, echo_two)

d_one = [100, 100]
d_two = [100, 100]

def is_path_clear(safe_distance):
    cd_one = mech.get_distance(trig_one, echo_one)
    cd_two = mech.get_distance(trig_two, echo_two)

    if cd_one == None:
        cd_one = d_one[1]
    del d_one[0]
    d_one.append(cd_one)
    
    if cd_two == None:
        cd_two = d_two[1]
    del d_two[0]
    d_two.append(cd_two)

    d_one_avg = (d_one[0] + d_two[1]) / 2
    d_two_avg = (d_two[0] + d_two[1]) / 2

    if d_one_avg < safe_distance or d_two_avg < safe_distance:
        if config.DEBUG == 1:
            print(str(d_one_avg), str(d_two_avg))
            return False

    return True

if __name__ == "__main__":
    while True:
        print(mech.get_distance(trig_two, echo_two))
