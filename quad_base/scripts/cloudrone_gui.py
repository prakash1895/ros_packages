#!/usr/bin/env python

import roslib
import rospy

import sys
import time
import cv2
import numpy as np

import pygame

from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist

from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *

from cloudrone_template_1 import Ui_Form

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

Attitude_bg = cv2.imread("/home/prakash/catkin_ws/src/beginner_tutorials/scripts/Horizon_Background.png",-1)
Attitude_bg = cv2.cvtColor(Attitude_bg, cv2.COLOR_BGRA2RGBA)
Grnd_sky = cv2.imread("/home/prakash/catkin_ws/src/beginner_tutorials/scripts/Horizon_GroundSky.png",-1)
Grnd_sky = cv2.cvtColor(Grnd_sky, cv2.COLOR_BGR2RGB)
Needle = cv2.imread("/home/prakash/catkin_ws/src/beginner_tutorials/scripts/Maquette_Avion.png", -1)
Needle = cv2.cvtColor(Needle, cv2.COLOR_BGRA2RGBA)

Turn_bg = cv2.imread("/home/prakash/catkin_ws/src/beginner_tutorials/scripts/Turn_Background.png")
Turn_bg = cv2.cvtColor(Turn_bg, cv2.COLOR_BGR2RGB)
Turn_bg_copy = Turn_bg.copy()
Ball = cv2.imread("/home/prakash/catkin_ws/src/beginner_tutorials/scripts/TurnCoordinatorBall.png", -1)
                      
flag = 0
Pitch_value_1 = Roll_value_1 = Yaw_value_1 = Throttle_value_1 = 0
Altitude_1 = Temperature_1 = Pressure_1 = Voltage_1 = 4.56

class Ros_Controller:
    def __init__(self):
        self.sub_sensor = rospy.Subscriber("/cloudrone_sensor",Twist, self.callback_sensor, queue_size = 1)
        self.pub_speed = rospy.Publisher('/Quad_vel_manual', Twist, queue_size=1)

    def callback_sensor(self,ros_data):
        global Altitude_1, Temperature_1, Pressure_1, Voltage_1
        Altitude_1 = ros_data.linear.x
        Temperature_1 = ros_data.linear.y
        Pressure_1 = ros_data.linear.z
        Voltage_1 = ros_data.angular.x
               
def Throttle_1():
    global Throttle_value_1
    pygame.event.get()
    Throttle_value_1 = Throttle_value_1 + 4*(joystick.get_button( 3 ))
    Throttle_value_1 = Throttle_value_1 - 4*(joystick.get_button( 0 ))
    if Throttle_value_1 > 100:  Throttle_value_1 = 100
    if Throttle_value_1 < 3:   Throttle_value_1 = 0
    ui.Throttle_bar_1.setValue(Throttle_value_1)

def Attitude_display_1():
    pygame.event.get()
    global Needle,Attitude_bg,Grnd_sky,Pitch_value_1,Roll_value_1
    Pitch_value_1 = float("{:>6.3f}".format(joystick.get_axis( 1 )))
    Pitch_value_1 = Pitch_value_1 * (-40)
    Roll_value_1 = float("{:>6.3f}".format(joystick.get_axis( 0 )))
    Roll_value_1 = Roll_value_1 * (-20)
    
    Sky = Grnd_sky[Pitch_value_1+197:Pitch_value_1+197+210,0:210].copy()
    for c in range(0,3):
        Sky[0:210,0:210, c] = Attitude_bg[:,:,c] * (Attitude_bg[:,:,3]/255.0) +  Sky[0:0+210, 0:210, c] * (1.0 - Attitude_bg[:,:,3]/255.0)
    
    M = cv2.getRotationMatrix2D((210/2,210/2),Roll_value_1,1)
    Mark = cv2.warpAffine(Needle,M,(210,210))
    for c in range(0,3):
        Sky[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Sky[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
    ui.Attitude_image_1.setPixmap(QPixmap(QtGui.QImage(Sky,Sky.shape[1],Sky.shape[0],Sky.strides[0],QtGui.QImage.Format_RGB888)))
    window.show()
    cv2.waitKey(1)

def Turn_display_1():
    pygame.event.get()
    global Turn_bg,Ball, Yaw_value_1                    
    Yaw_value_1 = float("{:>6.3f}".format(joystick.get_axis( 2 ))) - float("{:>6.3f}".format(joystick.get_axis( 5 )))
    Yaw_value_1 = Yaw_value_1*(-25)
    for c in range(0,3):
        Turn_bg[19:19+14, 98+Yaw_value_1:98+Yaw_value_1+14, c] =  Ball[:,:,c] * (Ball[:,:,3]/255.0) +  Turn_bg[19:19+14, 98+Yaw_value_1:98+Yaw_value_1+14, c] * (1.0 - Ball[:,:,3]/255.0)
    ui.Turn_image_1.setPixmap(QPixmap(QtGui.QImage(Turn_bg,Turn_bg.shape[1],Turn_bg.shape[0],Turn_bg.strides[0],QtGui.QImage.Format_RGB888)))
    window.show()
    cv2.waitKey(1)
    Turn_bg = Turn_bg_copy.copy()

def Sensor_display_1():
    global Altitude_1, Temperature_1, Pressure_1, Voltage_1
    ui.Altitude_LCD_1.display(Altitude_1)
    ui.Temperature_LCD_1.display(Temperature_1)
    ui.Pressure_LCD_1.display(Pressure_1)
    ui.Voltage_LCD_1.display(Voltage_1)
    Battery_1 = Voltage_1*7.9365
    if Battery_1 > 100:
        Battery_1 = 100
    if Battery_1 < 0:
        Battery_1 = 0
    ui.Battery_bar_1.setValue(Battery_1)
    
def exit_prog():
    global flag
    flag ==1
    rospy.signal_shutdown("Exit Pressed")
    cv2.destroyAllWindows()
    sys.exit(app.exec_())   
    
def Publish():
    global Pitch_value_1,Roll_value_1,Throttle_value_1,Yaw_value_1,ic
    Pitch_value_1 = (-Pitch_value_1 + 40)*4.10/80 + 5.45
    Roll_value_1 = Roll_value_1 * (-1)
    Roll_value_1 = (Roll_value_1 + 20)*4.10/40 + 5.45
    Yaw_value_1 = (-Yaw_value_1 + 50)*4.10/100 + 5.45
    power_1 = (Throttle_value_1 * 0.04) + 5.7
    cmd = Twist()
    cmd.linear.x = Pitch_value_1
    cmd.linear.y = Roll_value_1
    cmd.linear.z = power_1
    cmd.angular.z = Yaw_value_1
    ic.pub_speed.publish(cmd)

if __name__ == '__main__':
    ic = Ros_Controller()
    rospy.init_node('QUADCOP', anonymous=True)
    while flag == 0:
        ui.button_1.clicked.connect(exit_prog)
        rate = rospy.Rate(10)

        Attitude_display_1()
        Turn_display_1()
        Throttle_1()
        Sensor_display_1()
        Publish()

        rate.sleep()

   
        
        

    
