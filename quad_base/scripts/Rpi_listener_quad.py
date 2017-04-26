#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #Raspberry pi 2 or higher

GPIO.setup(6,GPIO.OUT) #configuring GPIO pins as output
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

Roll_pwm = GPIO.PWM(6,50)   #configuring GPIO pins as PWM outputs
Pitch_pwm = GPIO.PWM(13,50)
Throttle_pwm = GPIO.PWM(19,50)
Yaw_pwm = GPIO.PWM(26,50)

def callback(data):
    Pitch = data.linear.x  #receving inputs from joystick
    Roll = data.linear.y
    Throttle = data.linear.z
    Yaw = data.angular.z

    Roll_pwm.ChangeDutyCycle(Roll)  
    Pitch_pwm.ChangeDutyCycle(Pitch)
    Throttle_pwm.ChangeDutyCycle(Throttle)
    Yaw_pwm.ChangeDutyCycle(Yaw)
    
    print "P :"+str(Pitch)+" R :"+str(Roll)+" Y :"+str(Yaw)+" T :"+str(Throttle)

def listener():

    rospy.init_node('Quad_listener', anonymous=True)
    
    Roll_pwm.start(4)
    Pitch_pwm.start(4)
    Throttle_pwm.start(4)
    Yaw_pwm.start(4)
    
    rospy.Subscriber("/Quad_vel_manual", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
try:
    listener()
except KeyboardInterrupt:  # Press Ctrl+c to exit
    Roll_pwm.stop()
    Pitch_pwm.stop()
    Throttle_pwm.stop()
    Yaw_pwm.stop()
    GPIO.cleanup()
