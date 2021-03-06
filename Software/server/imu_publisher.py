#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import smbus            
import math             

import rospy
from sensor_msgs.msg import Imu

DEV_ADDR = 0x68         

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
PWR_MGMT_1 = 0x6b       
PWR_MGMT_2 = 0x6c       

bus = smbus.SMBus(1)
                        
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

def read_byte(adr):
    return bus.read_byte_data(DEV_ADDR, adr)

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):         
        return -((65535 - val) + 1)
    else:                       
        return val

def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      
    return x

def get_gyro_data_lsb():
    x = read_word_sensor(GYRO_XOUT)
    y = read_word_sensor(GYRO_YOUT)
    z = read_word_sensor(GYRO_ZOUT)
    return [x, y, z]

def get_gyro_data_deg():
    x,y,z = get_gyro_data_lsb()
    x = x / 131.0
    y = y / 131.0
    z = z / 131.0
    return [x, y, z]

def get_gyro_data_rad():
    x,y,z = get_gyro_data_deg()
    x = 2 * math.pi * (x / 360)
    y = 2 * math.pi * (y / 360)
    z = 2 * math.pi * (z / 360)
    return [x, y, z]


def get_accel_data_lsb():
    x = read_word_sensor(ACCEL_XOUT)
    y = read_word_sensor(ACCEL_YOUT)
    z = read_word_sensor(ACCEL_ZOUT)
    return [x, y, z]

def get_accel_data_g():
    x,y,z = get_accel_data_lsb()
    x = x / 16384.0
    y = y / 16384.0
    z = z / 16384.0
    return [x, y, z]

def get_accel_data_mpss():
    x,y,z = get_accel_data_g()
    x = x * 9.80665
    y = y * 9.80665
    z = z * 9.80665
    return [x, y, z]

def talker():
    pub = rospy.Publisher('/imu',Imu)
    rospy.init_node('imu_publisher')
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        imu_data = Imu()

        gyro_x,gyro_y,gyro_z = get_gyro_data_rad()
        accel_x,accel_y,accel_z = get_accel_data_mpss()

        imu_data.angular_velocity = [gyro_x,gyro_y,gyro_z]
        imu_data.linear_acceleration = [accel_x,accel_y,accel_z]

        rospy.loginfo()
        pub.publish(imu_data)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
