#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def callback(msg):
    print msg   #ALL
    #print msg.linear #linear only
    #print msg.angular #angular only
    #print msg.linear.x,y,z #linear and x or y or z

rospy.init_node('topic_subscriber')

sub = rospy.Subscriber('/cmd_vel',Twist,callback)

rospy.spin()
