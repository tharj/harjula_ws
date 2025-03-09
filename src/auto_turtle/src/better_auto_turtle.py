#! /usr/bin/python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import pi
import random

turning = 0
start_time = None


def cb(msg):
    global start_time, turning

    vel_msg = Twist()

    near_wall = False
    random_speed = 0

    if msg.x > 10 or msg.y > 10 or msg.x < 1 or msg.y < 1: # check wall vicinity from coordinates
        near_wall = True # set flag

    if turning == 0 and near_wall: # if not yet turning, but close to wall
        turning = 1 # set turn flag
        start_time = rospy.get_time() # start time for comparison later 
        rospy.loginfo('Start turning') # debug
        random_speed = random.uniform(-0.7, 0.7) 

    if turning == 1: 
        vel_msg.linear.x = 0.0  # Stop moving forward
        vel_msg.angular.z = pi + random_speed # set angular velocity to turn

        elapsed_time = rospy.get_time() - start_time
        rospy.loginfo(f'Elapsed time: {elapsed_time}')

        if elapsed_time > 1.0: # rospy.sleep doesnt work
            turning = 0 # flag down
            vel_msg.linear.x = 2.0 # linear move back up
            vel_msg.angular.z = random.uniform(-1, 1)  # Random angular speed
            rospy.loginfo('Turning completed')

    else: # default linear moving state
        vel_msg.linear.x = 2.0 
        vel_msg.angular.z = -4 if (random.uniform(-1, 1) < 0) else 4 

    velocity_publisher.publish(vel_msg)


# Initialize node, publisher, and subscriber
rospy.init_node('auto_turtle')
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
rospy.Subscriber('/turtle1/pose', Pose, cb)

rospy.spin()