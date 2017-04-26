import numpy as np
import cv2
import pygame

cap = cv2.VideoCapture(0)
zoom = 2

_, frame = cap.read()
cv2.imshow('frame',frame)

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

rows = frame.shape[0]
cols = frame.shape[1]
limits = [0,10,0,10]
y = rows/2
x = cols/2

def limit():
    global zoom,limits,rows,cols,x,y
    if x < 50:
        x = 50
    elif x > cols-50:
        x = cols-50
    if y < 50:
        y = 50
    elif y > rows-50:
        y = rows-50
    
    limits[0] = y-int(rows/zoom)
    limits[1] = y+int(rows/zoom)
    limits[2] = x-int(cols/zoom)
    limits[3] = x+int(cols/zoom)
    
    if limits[0]<0:
        limits[0] = 0
    if limits[1] > rows:
        limits[1] = rows
    if limits[2]<0:
        limits[2] = 0
    if limits[3] > cols:
        limits[3] = cols
        
def zoom_roi():
    global zoom
    if zoom == 8:
        roi = frame[limits[0]:limits[1],limits[2]:limits[3]]
        roi = cv2.pyrUp(roi)
        roi = cv2.pyrUp(roi)
        cv2.imshow('zoom',roi)
        cv2.startWindowThread()
        cv2.waitKey(1)
        cv2.rectangle(frame,(limits[2],limits[0]),(limits[3],limits[1]),(0,0,255),2)
    elif zoom == 4:
        roi = frame[limits[0]:limits[1],limits[2]:limits[3]]
        roi = cv2.pyrUp(roi)
        cv2.imshow('zoom',roi)
        cv2.startWindowThread()
        cv2.waitKey(1)
        cv2.rectangle(frame,(limits[2],limits[0]),(limits[3],limits[1]),(0,0,255),2)
        
while True:
    ret, frame = cap.read()
    pygame.event.get()

    if joystick.get_button(4) == 1:
        zoom = 4
    elif joystick.get_button(5) == 1:
        zoom = 8
    hat = joystick.get_hat(0)
    x = x + 10*hat[0]
    y = y - 10*hat[1]
    limit()  
    zoom_roi()
    
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
