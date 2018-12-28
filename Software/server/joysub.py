#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import Joy
import sys

def callback(msg):
    left_X = msg.axes[0] * -1
    left_Y = msg.axes[1]

    print left_X
    print left_Y

def listener():
    rospy.init_node('joystick_subscriber')
    sub = rospy.Subscriber('/joy',Joy,callback)
    print sub
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        sys.exit()
