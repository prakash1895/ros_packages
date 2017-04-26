#!/usr/bin/env python

import rospy
import roslib
import sys

from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import Adafruit_BMP.BMP085 as BMP085

adc = Adafruit_ADS1x15.ADS1015()
altimeter = BMP085.BMP085()

GPIO.setmode(GPIO.BCM) #Raspberry pi 2 or higher
GPIO.setup(6,GPIO.OUT) #configuring GPIO pins as output
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

Roll_pwm = GPIO.PWM(6,50)   #configuring GPIO pins as PWM outputs
Pitch_pwm = GPIO.PWM(13,50)
Throttle_pwm = GPIO.PWM(19,50)
Yaw_pwm = GPIO.PWM(26,50)

class Quad_listener:
    
    def __init__(self):
        
        Roll_pwm.start(4)
        Pitch_pwm.start(4)
        Throttle_pwm.start(4)
        Yaw_pwm.start(4)
        
        self.manual_sub = rospy.Subscriber("/Quad_vel_manual", Twist, self.callback)
        self.sensor_pub = rospy.Publisher("/cloudrone_sensor", Twist, queue_size=1)

    def callback(self,data):
        try:
            Pitch = data.linear.x  #receving inputs from joystick
            Roll = data.linear.y
            Throttle = data.linear.z
            Yaw = data.angular.z

            Roll_pwm.ChangeDutyCycle(Roll)  
            Pitch_pwm.ChangeDutyCycle(Pitch)
            Throttle_pwm.ChangeDutyCycle(Throttle)
            Yaw_pwm.ChangeDutyCycle(Yaw)
    
            print "P :"+str(Pitch)+" R :"+str(Roll)+" Y :"+str(Yaw)+" T :"+str(Throttle)

            sensor_data = geometry_msgs.msg.Twist()
            
            sensor_data.linear.x = adc.read_adc(0,1)
            senosr_data.linear.y = altimeter.read_altitude()
            sensor_data.linear.z = altimeter.read_pressure()
            sensor_data.angular.x = altimeter.read_temperature()
            self.sensor_pub.publish(sensor_data)
        except:
            pass
        
def publish():
    global adc,altimeter,cloudrone
    sensor_data = geometry_msgs.msg.Twist()
            
    sensor_data.linear.x = adc.read_adc(0,1)
    senosr_data.linear.y = altimeter.read_altitude()
    sensor_data.linear.z = altimeter.read_pressure()
    sensor_data.angular.x = altimeter.read_temperature()
    cloudrone.sensor_pub.publish(sensor_data)

     
if __name__ == '__main__':
    cloudrone = Quad_listener()
    rospy.init_node('Quad_listener',anonymous=True)
    while not rospy.is_shutdown(():
        try:
            publish()
            rospy.spin()
        except rospy.ROSInterruptException:
            Roll_pwm.stop()
            Pitch_pwm.stop()
            Throttle_pwm.stop()
            Yaw_pwm.stop()
            GPIO.cleanup()

    
