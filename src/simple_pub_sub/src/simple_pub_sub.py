#! /usr/bin/python3

import rospy
from std_msgs.msg import String

topic_to_listen = 'simple_pub'

def cb(msg):
    message = f'Repub message from {topic_to_listen}: {msg}'
    pub.publish(message)

rospy.init_node('simple_pub_sub')
pub = rospy.Publisher('/simple_pub_sub', String, queue_size=10)
rospy.Subscriber(topic_to_listen, String, cb)
rospy.spin()