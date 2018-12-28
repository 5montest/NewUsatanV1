#!/usr/bin/env python2

import pigpio
import sys
import time
import rospy
from std_msgs.msg import Bool

A = 23

pi = pigpio.pi()
pi.set_mode(A, pigpio.INPUT)
pi.set_pull_up_down(A, pigpio.PUD_UP)

def talker():
    pub = rospy.Publisher('/motion_sensor', Bool)
    rospy.init_node('motion_sensor_publisher')
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        read_data =  pi.read(A)
        pub.publish(read_data)
        print(read_data)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
