#! /usr/bin/python3

import rospy
from std_msgs.msg import String

rospy.init_node('our_set_private_param_node', anonymous=True)

rospy.set_param('~this_is_private_starts_with_tilde', 'started_from_rospy')