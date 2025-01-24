#! /usr/bin/python3

import rospy
from std_msgs.msg import String

rospy.init_node('talker')
pub = rospy.Publisher('simple_pub', String)
rate = rospy.Rate(1)

while not rospy.is_shutdown():
    hello_str = 'Hello from ROS publisher'
    pub.publish(hello_str)
    rate.sleep()