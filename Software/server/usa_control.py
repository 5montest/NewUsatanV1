#!/usr/bin/env python2

import pigpio
import time
import math

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

l_pwm = 18
l_pin0 = 17
l_pin1 = 27
r_pwm = 19
r_pin0 = 13
r_pin1 = 6

freq = 1000
duty_max = 100000

class UsaControl:
    def __init__(self, pi):
        self.pi = pi
        self.linear = 0
        self.angular = 0
        self.l_duty = 0.0
        self.r_duty = 0.0
        self.old_linear = 0
        self.l_speed = 0
        self.r_speed = 0

    def callback(self, msg):
        self.old_linear = self.linear
        self.linear = msg.linear.x
        self.angular = msg.angular.z

        #print self.linear
        #print self.angular

    def callback_l(self, msg):
        self.l_speed = msg

    def callback_r(self, msg):
        self.r_speed = msg


    def listener(self):
        rospy.init_node('cmd_vel_subscriber')
        sub = rospy.Subscriber('/cmd_vel',Twist,self.callback)
        rps_r = rospy.Subscriber('/encoder_R',Float32,self.callback_r)
        rps_l = rospy.Subscriber('/encoder_L',Float32,self.callback_l)

        print sub

        # -------------------- MAIN LOOP ------------------------------
        while True:
            time.sleep(0.001)

            # Move forward
            if self.linear > 0:
                if (self.old_linear != self.linear):
                    self.l_duty = self.l_speed*duty_max
                    self.r_duty = self.r_speed*duty_max
                    self.old_linear = self.linear # Flag disable
                self.l_duty = self.l_duty - (self.l_speed - self.r_speed)/(2*math.pi)*duty_max
                self.r_duty = self.r_duty - (self.r_speed - self.l_speed)/(2*math.pi)*duty_max

                pi.write(l_pin0,0)
                pi.write(l_pin1,1)
                pi.hardware_PWM(l_pwm,freq,self.l_duty)
                pi.write(r_pin0,0)
                pi.write(r_pin1,1)
                pi.hardware_PWM(r_pwm,freq,self.r_duty)

                print("L : {}   \t  R : {}".format(self.l_duty, self.r_duty))
               
            # Move backward
            elif self.linear < 0:
                pi.write(l_pin0,1)
                pi.write(l_pin1,0)
                pi.hardware_PWM(l_pwm,freq,l_duty)
                pi.write(r_pin0,1)
                pi.write(r_pin1,0)
                pi.hardware_PWM(r_pwm,freq,r_duty)
               
            # Turn right
            elif self.angular > 0:
                pi.write(l_pin0,0)
                pi.write(l_pin1,1)
                pi.hardware_PWM(l_pwm,freq,l_duty)
                pi.write(r_pin0,0)
                pi.write(r_pin1,1)
                pi.hardware_PWM(r_pwm,freq,0)
               
            # Turn left
            elif self.angular < 0:
                pi.write(l_pin0,0)
                pi.write(l_pin1,1)
                pi.hardware_PWM(l_pwm,freq,0)
                pi.write(r_pin0,0)
                pi.write(r_pin1,1)
                pi.hardware_PWM(r_pwm,freq,r_duty)
               
            # Stop
            else:
                pi.write(l_pin0,0)
                pi.write(l_pin1,1)
                pi.hardware_PWM(l_pwm,freq,0)
                pi.write(r_pin0,0)
                pi.write(r_pin1,1)
                pi.hardware_PWM(r_pwm,freq,0)

        rospy.spin()

if __name__ == '__main__':
    try:
        pi = pigpio.pi()
        # Left config
        pi.set_mode(l_pwm,pigpio.OUTPUT)
        pi.set_mode(l_pin0,pigpio.OUTPUT)
        pi.set_mode(l_pin1,pigpio.OUTPUT)
        # Right config
        pi.set_mode(r_pwm,pigpio.OUTPUT)
        pi.set_mode(r_pin0,pigpio.OUTPUT)
        pi.set_mode(r_pin1,pigpio.OUTPUT)
        
        # Start control
        usa_control = UsaControl(pi)
        usa_control.listener()

    except KeyboardInterrupt:
        pi.write(l_pin0,0)
        pi.write(l_pin1,1)
        pi.write(r_pin0,0)
        pi.write(r_pin1,1)
        pi.hardware_PWM(l_pwm,freq,0)
        pi.hardware_PWM(r_pwm,freq,0)
        pi.stop()
