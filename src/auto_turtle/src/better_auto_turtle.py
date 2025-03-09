#! /usr/bin/python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import pi
import random

turning, direction, target_angle = 0,0,0

def cb(msg):
    global turning, target_angle, direction

    vel_msg = Twist()

    near_wall = False

    if msg.x > 10 or msg.y > 10 or msg.x < 1 or msg.y < 1: # check wall vicinity from coordinates
        near_wall = True # set flag

    if turning == 0 and near_wall: # if not yet turning, but close to wall
        turning = 1 # set turn flag
        rospy.loginfo('start turning') # debug

        if msg.x > 10: # RIGHT
            if msg.theta < 0: # downward
                target_angle = random.uniform(-0.2,0.2) + 0.75*-pi
                direction = -1
            else: # upward
                target_angle = random.uniform(-0.2,0.2) + 0.75*pi
                direction = 1
        elif msg.y > 10: # TOP
            if msg.theta > pi/2: #going right
                target_angle = random.uniform(-0.2,0.2) + 0.75*-pi
                direction = 1
            else:
                target_angle = random.uniform(-0.2,0.2) + 0.25*-pi
                direction = -1
        elif msg.x < 1: # LEFT
            if msg.theta < 0: # downward
                target_angle = random.uniform(-0.2,0.2) + 0.25*-pi
                direction = 1
                # target_angle = -(pi-msg.theta) + random_angle
            else: # upward
                target_angle = random.uniform(-0.2,0.2) + 0.25*pi
                direction = -1
        elif msg.y < 1: # BOTTOM
            if msg.theta > -pi/2: #going right
                target_angle = random.uniform(-0.2,0.2) + 0.25*pi
                direction = 1
            else:
                target_angle = random.uniform(-0.2,0.2) + 0.75*pi
                direction = -1

        rospy.loginfo(f'target_angle {target_angle}')
        rospy.loginfo(f'target_angle {direction}')

    if turning == 1: 
        vel_msg.linear.x = 0.0  # Stop moving forward
        vel_msg.angular.z = 3*direction # set angular velocity to turn 
        if abs(msg.theta - target_angle) < 0.05:
            turning = 0 # flag down
            vel_msg.linear.x = 4.0 # linear move back up
            vel_msg.angular.z = 0
            rospy.loginfo('turning completed')

    else: # default linear moving state
        vel_msg.linear.x = 4.0 
        vel_msg.angular.z = 0
        vel_msg.angular.z = -2 if (random.uniform(-1, 1) < 0) else 2

    velocity_publisher.publish(vel_msg)

rospy.init_node('auto_turtle')
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
rospy.Subscriber('/turtle1/pose', Pose, cb)

rospy.spin()