import numpy as np
import cv2

cap = cv2.VideoCapture(0)
zoom = 2
limits = [0,10,0,10]
_, frame = cap.read()
cv2.imshow('frame',frame)
rows = frame.shape[0]
cols = frame.shape[1]

def centre(event,x,y,flags,param):
    global zoom,limits,rows,cols
    if (event == cv2.EVENT_LBUTTONDOWN):        
        zoom  = 4
    if (event == cv2.EVENT_RBUTTONDOWN):        
        zoom  = 8
    limits[0] = y-int(rows/zoom)
    limits[1] = y+int(rows/zoom)
    limits[2] = x-int(cols/zoom)
    limits[3] = x+int(cols/zoom)
    #print x
    if limits[0]<0:
        limits[0] = 0
    if limits[1] > rows:
        limits[1] = rows
    if limits[2]<0:
        limits[2] = 0
    if limits[3] > cols:
        limits[3] = cols
        
cv2.setMouseCallback('frame',centre)         
while(True):
    ret, frame = cap.read()
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
    
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
