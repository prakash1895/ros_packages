#!/usr/bin/env python

import roslib
import rospy

import sys
import time
import pygame

from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()
      
flag = 0
Pitch_value = Roll_value = Yaw_value = Throttle_value = 0

def Publish(): 
    pub_speed= rospy.Publisher('/Quad_vel_manual', Twist, queue_size=10)
    rospy.init_node('Quadcop', anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown():

        global Pitch_value,Roll_value,Throttle_value,Yaw_value,ic
        pygame.event.get()
    
        Throttle_value = Throttle_value + 1.5*(joystick.get_button( 3 ))
        Throttle_value = Throttle_value - 1.5*(joystick.get_button( 0 ))
        if Throttle_value > 100:  Throttle_value2= 100
        if Throttle_value < 1:   Throttle_value = 0
    
        Pitch_value = float("{:>6.3f}".format(joystick.get_axis( 1 )))
        Roll_value = float("{:>6.3f}".format(joystick.get_axis( 0 )))
        Yaw_value = float("{:>6.3f}".format(joystick.get_axis( 2 ))) - float("{:>6.3f}".format(joystick.get_axis( 5 )))

        Roll_value = 3*(Roll_value) + 7
        Pitch_value = 3*(Pitch_value) + 7
        Yaw_value = 1.5*(Yaw_value) + 7
        Power = 0.06*(Throttle_value) + 4

        if Power > 10.0:    Power = 10.0
        if Power < 4.0:     Power = 4.0
        
        print Pitch_value,Roll_value,Yaw_value,Power

        cmd = Twist()
        cmd.linear.x = Pitch_value
        cmd.linear.y = Roll_value
        cmd.linear.z = Power
        cmd.angular.z = Yaw_value
        pub_speed.publish(cmd)

        rate.sleep()
        
if __name__ == '__main__':
    try:
        Publish()
    except rospy.ROSInterruptException:
        pass
