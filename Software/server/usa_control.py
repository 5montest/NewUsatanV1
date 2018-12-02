#!/usr/bin/env python2

import pigpio

import rospy
from geometry_msgs.msg import Twist

l_pwm = 18
l_pin0 = 17
l_pin1 = 27
r_pwm = 19
r_pin0 = 13
r_pin1 = 6

freq = 1000
duty = 100000

pi = pigpio.pi()
pi.set_mode(l_pwm,pigpio.OUTPUT)
pi.set_mode(l_pin0,pigpio.OUTPUT)
pi.set_mode(l_pin1,pigpio.OUTPUT)
pi.set_mode(r_pwm,pigpio.OUTPUT)
pi.set_mode(r_pin0,pigpio.OUTPUT)
pi.set_mode(r_pin1,pigpio.OUTPUT)

def callback(msg):
    linear = msg.linear.x
    angular = msg.angular.z

    print linear
    print angular

    if linear > 0:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,duty)
        pi.hardware_PWM(r_pwm,freq,duty)
        
    elif linear < 0:
        pi.write(l_pin0,1)
        pi.write(l_pin1,0)
        pi.write(r_pin0,1)
        pi.write(r_pin1,0)
        pi.hardware_PWM(l_pwm,freq,duty)
        pi.hardware_PWM(r_pwm,freq,duty)
        
    elif angular > 0:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,duty)
        pi.hardware_PWM(r_pwm,freq,0)
        
    elif angular < 0:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,duty)
        
    else:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,0)

def listener():
    rospy.init_node('cmd_vel_subscriber')
    sub = rospy.Subscriber('/turtle1/cmd_vel',Twist,callback)
    print sub
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        pi.stop()
