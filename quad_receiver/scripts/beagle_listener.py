#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import mraa
import time

Roll_pwm = mraa.Pwm(45) #P8.45
Roll_pwm.period_ms(20)

Pitch_pwm = mraa.Pwm(46) #P8.46
Pitch_pwm.period_ms(20)

Throttle_pwm = mraa.Pwm(67) #P9.21
Throttle_pwm.period_ms(20)

Yaw_pwm = mraa.Pwm(68)  #P9.22
Yaw_pwm.period_ms(20)

Roll_pwm.write(0.05)
Pitch_pwm.write(0.05)
Throttle_pwm.write(0.05)
Yaw_pwm.write(0.05)

def callback(data):
    Pitch = data.linear.x  #receving inputs from joystick
    Roll = data.linear.y
    Throttle = data.linear.z
    Yaw = data.angular.z

    Roll_pwm.write(Roll/100.0)
    Pitch_pwm.write(Pitch/100.0)
    Throttle_pwm.write(Throttle/100.0)
    Yaw_pwm.write(Yaw/100.0)

    print "P :"+str(Pitch)+" R :"+str(Roll)+" Y :"+str(Yaw)+" T :"+str(Throttle)

def listener():

    rospy.init_node('Quad_listener', anonymous=True)

    Roll_pwm.enable(True)
    Pitch_pwm.enable(True)
    Throttle_pwm.enable(True)
    Yaw_pwm.enable(True)

    rospy.Subscriber("/Quad_vel_manual", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:  # Press Ctrl+c to exit
        pass
