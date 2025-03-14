#! /usr/bin/python3

import rospy
import tf2_ros
import geometry_msgs.msg
from turtlesim.srv import Spawn
import math

if __name__ == '__main__':
    rospy.init_node('turtle_listener')
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    turtle_name = rospy.get_param('~turtle')
    x,y,theta = 6,1,9 
    spawner(x,y,theta,turtle_name)

    turtle_vel = rospy.Publisher(f'/{turtle_name}/cmd_vel', 
                                 geometry_msgs.msg.Twist, 
                                 queue_size=1)
    
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try: 
            trans = tf_buffer.lookup_transform(turtle_name, 'turtle1', rospy.Time())
        except(tf2_ros.LookupException,
               tf2_ros.ConnectivityException,
               tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        
        msg = geometry_msgs.msg.Twist()
        msg.linear.x = 0.5* math.sqrt(trans.transform.translation.x**2 + trans.transform.translation.y**2)
        msg.angular.z = 4* math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        turtle_vel.publish(msg)
        rate.sleep()