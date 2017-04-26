#!/usr/bin/env python

import sys, time
import numpy as np
import cv2
import roslib
import rospy
import pygame
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Vector3
from python_qt_binding import QtGui,QtCore
from geometry_msgs.msg import Twist
from python_qt_binding.QtGui import *
from Template import Ui_Form
#from Test import *
VERBOSE=False

Ball = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/TurnCoordinatorBall.png", -1)
T_Backgrnd = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/Turn_Background.png")
T_Backgrnd = cv2.cvtColor(T_Backgrnd, cv2.COLOR_BGR2RGB)
T_Backgrnd_copy = T_Backgrnd.copy()
Wheel = cv2.imread("/home/adisron/catkin_ws/src/beginner_tutorials/scripts/HeadingWeel.png", -1)
Hea_Backgrnd = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/HeadingIndicator_Background.png")
Hea_Backgrnd = cv2.cvtColor(Hea_Backgrnd, cv2.COLOR_BGR2RGB)
Hea_Backgrnd_copy = Hea_Backgrnd.copy()
Needle = cv2.imread("/home/adisron/catkin_ws/src/beginner_tutorials/scripts/Maquette_Avion.png", -1)
Needle = cv2.cvtColor(Needle, cv2.COLOR_BGR2RGB)
H_Backgrnd = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/Horizon_Backgroung.png",-1)
H_Backgrnd = cv2.cvtColor(H_Backgrnd, cv2.COLOR_BGR2RGB)
Grnd_sky = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/Horizon_GroundSky.png")
Grnd_sky = cv2.cvtColor(Grnd_sky, cv2.COLOR_BGR2RGB)
Grnd_sky_copy = Grnd_sky.copy()

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)

latitude = longitude = 0
frame = np.zeros((480,640,3), np.uint8)

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()
        
Yaw = Pitch = Roll = throttle = flag = 0
Yaw_auto = Pitch_auto = Roll_auto = 0
zoom = 1
limits = [0,10,0,10]
rows = 480
cols = 640
x = rows/2
y = cols/2
num = 1

class My_GUI:

    def __init__(self):        
        #self.Cam = rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage, self.callback_Cam,  queue_size = 1)
        self.Cam = rospy.Subscriber("/camera/image/compressed",CompressedImage, self.callback_Cam,  queue_size = 1)
        self.GPS = rospy.Subscriber("/GPS",Vector3, self.callback_GPS,  queue_size = 1)
        self.Orient = rospy.Subscriber("/Orientation",Vector3, self.callback_Orient,  queue_size = 1)
        self.pub_speed = rospy.Publisher('/Quad_vel_manual', Twist, queue_size=1)
        
    def callback_Cam(self, ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        global frame
        frame = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def callback_GPS(self, ros_data):
        global latitude,longitude
        latitude = ros_data.x
        longitude = ros_data.y

    def callback_Orient(self, ros_data):
        global Pitch_auto,Roll_auto,Yaw_auto,Pitch,Roll,Yaw
        Pitch_auto = ros_data.x
        Roll_auto = ros_data.y
        Yaw_auto = ros_data.z
        
def Power():
    global throttle
    pygame.event.get()
    throttle = throttle + 4*(joystick.get_button( 3 ))
    throttle = throttle - 4*(joystick.get_button( 0 ))
    if throttle > 100:  throttle = 100
    if throttle < 3:   throttle = 0
    ui.Throttle.setValue(throttle)
    
            
def Attitude():
    pygame.event.get()
    global Needle,H_Backgrnd,Grnd_sky,Pitch,Roll,Sky,flag
    Pitch = float("{:>6.3f}".format(joystick.get_axis( 4 )))
    Pitch = Pitch * (-40)
    Roll = float("{:>6.3f}".format(joystick.get_axis( 3 )))
    Roll = Roll * (-20)
    
    Sky = Grnd_sky[Pitch+197:Pitch+197+210,0:210].copy()
    for c in range(0,3):
        Sky[0:210,0:210, c] = H_Backgrnd[:,:,c] * (H_Backgrnd[:,:,3]/255.0) +  Sky[0:0+210, 0:210, c] * (1.0 - H_Backgrnd[:,:,3]/255.0)
    
    M = cv2.getRotationMatrix2D((210/2,210/2),Roll,1)
    Mark = cv2.warpAffine(Needle,M,(210,210))
    for c in range(0,3):
        Sky[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Sky[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
        flag = 1
    ui.Attitude_Image.setPixmap(QPixmap(QtGui.QImage(Sky,Sky.shape[1],Sky.shape[0],Sky.strides[0],QtGui.QImage.Format_RGB888)))

def Heading():
    global Hea_Backgrnd,Hea_Backgrnd_copy,Yaw_auto
    M = cv2.getRotationMatrix2D((210/2,210/2),Yaw_auto,1)
    Mark = cv2.warpAffine(Wheel,M,(210,210))
    for c in range(0,3):
        Hea_Backgrnd[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Hea_Backgrnd[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
    ui.Heading_Image.setPixmap(QPixmap(QtGui.QImage(Hea_Backgrnd,Hea_Backgrnd.shape[1],Hea_Backgrnd.shape[0],Hea_Backgrnd.strides[0],QtGui.QImage.Format_RGB888)))
    Hea_Backgrnd = Hea_Backgrnd_copy.copy()

def Turn():
    pygame.event.get()
    global T_Backgrnd,T_Backgrnd_copy,Yaw
    Yaw = float("{:>6.3f}".format(joystick.get_axis( 2 ))) - float("{:>6.3f}".format(joystick.get_axis( 5 )))
    Yaw = Yaw*(-25)
    for c in range(0,3):
        T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] =  Ball[:,:,c] * (Ball[:,:,3]/255.0) +  T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] * (1.0 - Ball[:,:,3]/255.0)
    ui.Turn_Image.setPixmap(QPixmap(QtGui.QImage(T_Backgrnd,T_Backgrnd.shape[1],T_Backgrnd.shape[0],T_Backgrnd.strides[0],QtGui.QImage.Format_RGB888)))
    T_Backgrnd = T_Backgrnd_copy.copy()
    cv2.waitKey(1)
    
def display():
    global ui,roi,zoom_flag
    temp =  roi.shape[0]/(1.0*roi.shape[1])
    if temp > 75:
        frame_main = cv2.resize(roi,(int(624/temp),624))
    elif temp < 75:
        frame_main = cv2.resize(roi,(832,int(832*temp)))
    else:
        frame_main = cv2.resize(roi,(832,624))
    ui.Frame.setPixmap(QPixmap(QtGui.QImage(frame_main,frame_main.shape[1],frame_main.shape[0],frame_main.strides[0],QtGui.QImage.Format_RGB888)))
    window.show()
    cv2.waitKey(1)

def display_frame():
    global ui,frame
    frame_main = cv2.resize(frame,(832,624))
    ui.Frame.setPixmap(QPixmap(QtGui.QImage(frame_main,frame_main.shape[1],frame_main.shape[0],frame_main.strides[0],QtGui.QImage.Format_RGB888)))
    window.show()
    cv2.waitKey(1)

def GPS():
    global ui,latitude,longitude
    ui.Latitude_LCD.display(latitude)
    ui.Lonigitude_LCD.display(longitude)
    
def Zoom():
    global limits,frame,zoom,roi,rows,cols,x,y
    pygame.event.get()
    if joystick.get_button(4) == 1:    zoom -= 1
    elif joystick.get_button(5) == 1:  zoom += 1
    if zoom < 1:    zoom = 1
    
    hat = joystick.get_hat(0)
    x = x + 30*hat[0]
    y = y - 30*hat[1]

    if x < 50:         x = 50
    elif x > cols-50:  x = cols-50
    if y < 50:         y = 50
    elif y > rows-50:  y = rows-50
    
    limits[0] = y-int(rows/zoom)
    limits[1] = y+int(rows/zoom)
    limits[2] = x-int(cols/zoom)
    limits[3] = x+int(cols/zoom)
 
    if limits[0]<0:         limits[0] = 0
    if limits[1] > rows:    limits[1] = rows
    if limits[2]<0:         limits[2] = 0
    if limits[3] > cols:    limits[3] = cols

    roi = frame[limits[0]:limits[1],limits[2]:limits[3]]
    cv2.rectangle(frame,(limits[2],limits[0]),(limits[3],limits[1]),(0,0,255),2)
    frame_Zoom = cv2.resize(frame,(320,240))
    ui.Pressure_LCD_2.display(zoom)
    ui.Frame_Zoom.setPixmap(QPixmap(QtGui.QImage(frame_Zoom,frame_Zoom.shape[1],frame_Zoom.shape[0],frame_Zoom.strides[0],QtGui.QImage.Format_RGB888)))

def Mode():
    global num
    pygame.event.get()
    if joystick.get_button(7) == 1:
        num = num*(-1)
    if num == 1:
        ui.Display.setText("MANUAL")
    elif num == -1:
        ui.Display.setText("AUTOMATIC")

def Publish():
    global Pitch,Roll,ic,num,throttle,Yaw
    Pitch = (-Pitch + 40)*4.10/80 + 5.45
    Roll = Roll * (-1)
    Roll = (Roll + 20)*4.10/40 + 5.45
    Yaw = (-Yaw + 50)*4.10/100 + 5.45
    power = (throttle * 0.04) + 5.7
    cmd = Twist()
    cmd.linear.x = Pitch
    cmd.linear.y = Roll
    cmd.linear.z = power
    cmd.angular.x = num
    cmd.angular.z = Yaw
    #print cmd
    ic.pub_speed.publish(cmd)
    
if __name__ == '__main__':
    ic = My_GUI()
    rospy.init_node('QUADCOP', anonymous=True)
    while not rospy.is_shutdown():
        rate = rospy.Rate(40)
        Zoom()
        Attitude()
        GPS()
        Power()
        Heading()
        Turn()
        display()
        Mode()
        Publish()
        #display_frame()
        rate.sleep()

#PWM.stop(servo_pin)
#PWM.cleanup()
        
