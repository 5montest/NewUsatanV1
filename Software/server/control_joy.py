#!/usr/bin/env python2

import pigpio

import rospy
#from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

l_pwm = 18
l_pin0 = 17
l_pin1 = 27
r_pwm = 19
r_pin0 = 13
r_pin1 = 6

freq = 1000
duty = 1000000

pi = pigpio.pi()
pi.set_mode(l_pwm,pigpio.OUTPUT)
pi.set_mode(l_pin0,pigpio.OUTPUT)
pi.set_mode(l_pin1,pigpio.OUTPUT)
pi.set_mode(r_pwm,pigpio.OUTPUT)
pi.set_mode(r_pin0,pigpio.OUTPUT)
pi.set_mode(r_pin1,pigpio.OUTPUT)

def callback(msg):
    left_X = msg.axes[0] * -1
    left_Y = msg.axes[1]
    print left_X
    print left_Y

    if left_X == 0 and left_Y > 0:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,duty*left_Y)
        pi.hardware_PWM(r_pwm,freq,duty*left_Y)
        
    elif left_X > 0 and left_Y == 0:
        pi.write(l_pin0,1)
        pi.write(l_pin1,0)
        pi.write(r_pin0,1)
        pi.write(r_pin1,0)
        pi.hardware_PWM(l_pwm,freq,duty*left_X)
        pi.hardware_PWM(r_pwm,freq,0)
        
    elif left_X < 0 and left_Y == 0:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,duty*abs(left_X))
        
    elif left_X == 0 and left_Y < 0:
        pi.write(l_pin0,1)
        pi.write(l_pin1,0)
        pi.write(r_pin0,1)
        pi.write(r_pin1,0)
        pi.hardware_PWM(l_pwm,freq,duty*abs(left_Y))
        pi.hardware_PWM(r_pwm,freq,duty*abs(left_Y))

    elif left_X > 0 and left_Y > 0:
        if left_X > left_Y:
            distance = left_X
        else:
            distance = left_Y
        pi.write(l_pin0,1)
        pi.write(l_pin1,0)
        pi.write(r_pin0,1)
        pi.write(r_pin1,0)
        pi.hardware_PWM(l_pwm,freq,duty*abs(distance))
        pi.hardware_PWM(r_pwm,freq,duty*abs(distance))
    
    elif left_X < 0 and left_Y > 0:
        if left_X > left_Y:
            distance = left_X
        else:
            distance = left_Y
        pi.write(l_pin0,1)
        pi.write(l_pin1,0)
        pi.write(r_pin0,1)
        pi.write(r_pin1,0)
        pi.hardware_PWM(l_pwm,freq,duty*abs(distance))
        pi.hardware_PWM(r_pwm,freq,duty*abs(distance))

        
    else:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,0)

def listener():
    rospy.init_node('joystick_subscriber')
    sub = rospy.Subscriber('/joy',Joy,callback)
    print sub
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,0)
        pi.stop()
