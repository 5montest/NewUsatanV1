#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def callback(msg):
    linear_x = msg.linear.x
    angular_z = msg.angular.z

    print linear_x
    print angular_z

def listener():
    rospy.init_node('cmd_vel_subscriber')
    sub = rospy.Subscriber('/turtle1/cmd_vel',Twist,callback)
    print sub
    rospy.spin()

if __name__ == '__main__':
    listener()
