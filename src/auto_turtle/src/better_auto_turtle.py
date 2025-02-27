#! /usr/bin/python3

'''
Theta is the angle of the turtle in radians, 
    theta = 0, looking right
        from 0 to pi, looking up, pi/2 being straight up
    theta = pi or negative pi, looking left
        from 0 to negative pi, looking down, -pi/2 being straight down
'''

import rospy
from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist 
import random

pi = 3.141592653589793

def cb(msg):
    vel_msg = Twist()

    vel_msg.linear.x = 3
    vel_msg.angular.z = random.uniform(-1,1)
    turn_speed = 0
    random_angle = random.uniform(-0.5,0.5)

    # calculate turn speeds for different orientations
    if msg.x > 10: # RIGHT
        if msg.theta < 0: # downward
            turn_speed = -(pi-msg.theta) + random_angle
        else: # upward
            turn_speed = pi-msg.theta + random_angle
    elif msg.y > 10: # BOTTOM
        turn_speed = -msg.theta + random_angle
    elif msg.x < 1: # LEFT
        if msg.theta < 0: # downward
            turn_speed = -(pi-msg.theta) + random_angle
        else: # upward
            turn_speed = pi-msg.theta + random_angle
    elif msg.y < 1: # TOP
        turn_speed = -msg.theta + random_angle
    else:
        turn_speed = 0

    if turn_speed != 0: # if a wall detection has assigned a turn speed
            vel_msg.linear.x = 0 # stop linear movement
            vel_msg.angular.z = turn_speed # set angular speed from the previous pose theta
            velocity_publisher.publish(vel_msg) # publish speeds
            rospy.loginfo(f'msg.x: {msg.x}')
            rospy.sleep(1) # sleep 1 sec to turn
            vel_msg.angular.z = 0
            vel_msg.linear.x = 3 
            velocity_publisher.publish(vel_msg)
            rospy.sleep(0.1) # allow time to move away from the wall, to not trigger another turn_speed assignment immediately

    else:
        vel_msg.linear.x = 3
        vel_msg.angular.z = 0

    velocity_publisher.publish(vel_msg)

rospy.init_node('auto_turtle')
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1) 
rospy.Subscriber('/turtle1/pose', Pose, cb)

while not rospy.is_shutdown():
    rospy.spin()