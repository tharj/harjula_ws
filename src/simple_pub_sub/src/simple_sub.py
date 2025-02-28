#! /usr/bin/python3

import rospy
from std_msgs.msg import String

topic_to_listen = 'simple_pub'

def cb(msg):
    print(f'I heard | {msg} | from {topic_to_listen}')
    print('-----')

rospy.init_node('listener')
sub = rospy.Subscriber(topic_to_listen, String, cb)
rate = rospy.Rate(1)

rospy.spin()