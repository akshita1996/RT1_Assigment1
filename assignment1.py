#-------------IMPORT LIBRARIES----------------------
from __future__ import print_function
import time

#-------------IMPORT CLASS ROBOT--------------------
from sr.robot import *

#-------------DEFINING GOLBAL VARIABLES-------------

""" float: Threshold for the control of the linear distance"""
a_th = 2.3
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" instance of the class Robot"""  
R = Robot()
""" int: Maximum frontal distance that the robot must keep from golden tokens""" 
gold_th=1
""" float: Threshold for the activation of the grab routine"""
silver_th=1.5

#-------------DEFINING FUNCTIONS-------------

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70<token.rot_y<70:
            dist=token.dist
            rot_y=token.rot_y
    if dist==3:
        return -1, -1
    else:
        return dist, rot_y
   	
def grab_routine(rot_silver, dist_silver):
    if dist_silver <= d_th:
        print("Found it!")
        if R.grab():
	        print("Grabbed!")
        turn(20, 3)
        drive(15, 0.8)
        R.release()
        drive(-15,0.8)
        turn(-20,3)
    elif -a_th<=rot_silver<=a_th:
	    drive(40, 0.5) 
	    # print("Correct angle")
    elif rot_silver < -a_th: 
	    # print("Left a bit...")
	    turn(-5, 0.3)
    elif rot_silver > a_th:
	    # print("Right a bit...")
	    turn(+5, 0.3)

def turn_dir():
    left_dist=10
    for token in R.see():
        if token.dist < left_dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
            left_dist=token.dist
    right_dist=10
    for token in R.see():
        if token.dist < right_dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
            right_dist=token.dist
    if ( left_dist < right_dist ):
        turn_cloclwise = 1
    elif (left_dist > right_dist ):
        turn_cloclwise = -1
    return turn_cloclwise

def check_wall():
    dist=1
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -20<token.rot_y<20:
            dist=token.dist
    if dist==1:
        return -1
    else:
        return 1

def main():
    while 1:
        dist_silver, rot_silver = find_silver_token()
        is_wall_ahead = check_wall()
        if (dist_silver>silver_th) or (dist_silver==-1):
            if (is_wall_ahead == -1):
                drive(70,0.5)
            elif (is_wall_ahead == 1):
                drive(0,0.5)
                turn_cloclwise = turn_dir()
                turn(turn_cloclwise*70,0.4)
        elif dist_silver<silver_th and dist_silver!=-1:
            grab_routine(rot_silver, dist_silver)
		    			    		    				
#-----------------main() CALL-------------------
main()