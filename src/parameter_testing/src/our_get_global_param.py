#! /usr/bin/python3

import rospy
from std_msgs.msg import String

rospy.init_node('our_get_global_param_node')

msg = rospy.get_param('/this_is_global_starts_with_slash')
rospy.loginfo(msg)


