import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from Template import Ui_Form
import pygame
import cv2
import numpy as np

def nothing(x):
    pass

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

flag = 0
app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)
cap = cv2.VideoCapture(0)

cv2.namedWindow('CONTROLS')
cv2.createTrackbar('HEADING','CONTROLS',0,360,nothing)
Ball = cv2.imread("TurnCoordinatorBall.png", -1)
T_Backgrnd = cv2.imread("Turn_Background.png")
T_Backgrnd = cv2.cvtColor(T_Backgrnd, cv2.COLOR_BGR2RGB)
T_Backgrnd_copy = T_Backgrnd.copy()
Wheel = cv2.imread("HeadingWeel.png", -1)
Hea_Backgrnd = cv2.imread("HeadingIndicator_Background.png")
Hea_Backgrnd = cv2.cvtColor(Hea_Backgrnd, cv2.COLOR_BGR2RGB)
Hea_Backgrnd_copy = Hea_Backgrnd.copy()
Needle = cv2.imread("Maquette_Avion.png", -1)
Needle = cv2.cvtColor(Needle, cv2.COLOR_BGRA2RGBA)
H_Backgrnd = cv2.imread("Horizon_Backgroung.png",-1)
H_Backgrnd = cv2.cvtColor(H_Backgrnd, cv2.COLOR_BGRA2RGBA)
Grnd_sky = cv2.imread("Horizon_GroundSky.png")
Grnd_sky = cv2.cvtColor(Grnd_sky, cv2.COLOR_BGR2RGB)
Yaw = Pitch = Roll = throttle = 0

def Turn():
    global T_Backgrnd,T_Backgrnd_copy
    Yaw = float("{:>6.3f}".format(joystick.get_axis( 2 ))) - float("{:>6.3f}".format(joystick.get_axis( 5 )))
    Yaw = Yaw*(-25)
    for c in range(0,3):
        T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] =  Ball[:,:,c] * (Ball[:,:,3]/255.0) +  T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] * (1.0 - Ball[:,:,3]/255.0)
    ui.Turn_Image.setPixmap(QPixmap(QtGui.QImage(T_Backgrnd,T_Backgrnd.shape[1],T_Backgrnd.shape[0],T_Backgrnd.strides[0],QtGui.QImage.Format_RGB888)))
    T_Backgrnd = T_Backgrnd_copy.copy()
    cv2.waitKey(1)

def Heading():
    global Hea_Backgrnd,Hea_Backgrnd_copy
    Yaw = cv2.getTrackbarPos('HEADING','CONTROLS')
    M = cv2.getRotationMatrix2D((210/2,210/2),Yaw,1)
    Mark = cv2.warpAffine(Wheel,M,(210,210))
    for c in range(0,3):
        Hea_Backgrnd[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Hea_Backgrnd[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
    ui.Heading_Image.setPixmap(QPixmap(QtGui.QImage(Hea_Backgrnd,Hea_Backgrnd.shape[1],Hea_Backgrnd.shape[0],Hea_Backgrnd.strides[0],QtGui.QImage.Format_RGB888)))
    Hea_Backgrnd = Hea_Backgrnd_copy.copy()
    cv2.waitKey(1)

def Attitude():
    global Needle,H_Backgrnd,Grnd_sky,Pitch,Roll
    Pitch = float("{:>6.3f}".format(joystick.get_axis( 4 )))
    Pitch = Pitch * (-40)
    Roll = float("{:>6.3f}".format(joystick.get_axis( 3 )))
    Roll = Roll * (-20)
    #Pitch = cv2.getTrackbarPos('PITCH','CONTROLS')
    Sky = Grnd_sky[Pitch+197:Pitch+197+210,0:210].copy()
    for c in range(0,3):
        Sky[0:210,0:210, c] = H_Backgrnd[:,:,c] * (H_Backgrnd[:,:,3]/255.0) +  Sky[0:0+210, 0:210, c] * (1.0 - H_Backgrnd[:,:,3]/255.0)
    
    M = cv2.getRotationMatrix2D((210/2,210/2),Roll,1)
    Mark = cv2.warpAffine(Needle,M,(210,210))
    for c in range(0,3):
        Sky[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Sky[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
    ui.Attitude_Image.setPixmap(QPixmap(QtGui.QImage(Sky,Sky.shape[1],Sky.shape[0],Sky.strides[0],QtGui.QImage.Format_RGB888)))
    cv2.waitKey(1)

def Power():
    global throttle
    throttle += joystick.get_button( 3 )
    throttle -= joystick.get_button( 0 )
    if throttle > 90:
        throttle = 90
    if throttle < 0:
        throttle = 0
    ui.Throttle.setValue(throttle)

def Camera():
    global cap
    ret, cam = cap.read()
    cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(cam,(832,624))
    frame_Zoom = cv2.resize(cam,(320,240))
    ui.Frame.setPixmap(QPixmap(QtGui.QImage(frame,frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)))
    ui.Frame_Zoom.setPixmap(QPixmap(QtGui.QImage(frame_Zoom,frame_Zoom.shape[1],frame_Zoom.shape[0],frame_Zoom.strides[0],QtGui.QImage.Format_RGB888)))

def done():
    global flag
    flag = 1
    
while flag == 0:
    pygame.event.get()
    ui.EXIT.clicked.connect(done)
    Camera()
    Turn()
    Heading()
    Attitude()
    Power()
    window.show()
    cv2.waitKey(1)    

cap.release()
sys.exit(app.exec_())
cv2.destroyAllWindows()
