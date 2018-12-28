#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import pigpio
import sys
import math
import time
import rospy
from std_msgs.msg import Float32

A = 15
B = 7

pi = pigpio.pi()
pi.set_mode(A,pigpio.INPUT)
pi.set_mode(B,pigpio.INPUT)

pi.set_pull_up_down(A,pigpio.PUD_UP)
pi.set_pull_up_down(B,pigpio.PUD_UP)

global start
start =  0.0
global rps
rps = 0.0

def calc_value(gpio,level,tick):
    global start
    global rps
    if pi.read(B) == True:
        back = -1
    else:
        back = 1

    if start != 0.0:
        end = time.time()
        interval_time = end - start
        freq = 1.0/interval_time
        rps = freq * ((2 * math.pi) / 500) * back
    start = time.time()

cb = pi.callback(A,pigpio.FALLING_EDGE,calc_value)

def talker():
    pub = rospy.Publisher('/encoder_L',Float32)
    rospy.init_node('encoder_L_publisher')
    r = rospy.Rate(10)
    global start
    while not rospy.is_shutdown():
        diff = time.time() - start
        if diff < 1.0:
            pub.publish(rps)
            r.sleep()
        else:
            pub.publish(0.0)
            r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
