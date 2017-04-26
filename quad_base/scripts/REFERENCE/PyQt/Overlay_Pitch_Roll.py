import numpy as np
import cv2
import Image
'''
Sky[y_offset:y_offset+H_Backgrnd.shape[0], x_offset:x_offset+H_Backgrnd.shape[1], c] =
    H_Backgrnd[:,:,c] * (H_Backgrnd[:,:,3]/255.0) +  Sky[y_offset:y_offset+H_Backgrnd.shape[0], x_offset:x_offset+H_Backgrnd.shape[1], c] * (1.0 - H_Backgrnd[:,:,3]/255.0)
'''

def nothing(x):
    pass
cv2.namedWindow('CONTROLS')
cv2.createTrackbar('ROLL','CONTROLS',0,360,nothing)
cv2.createTrackbar('PITCH','CONTROLS',-85,85,nothing)
Needle = cv2.imread("Maquette_Avion.png", -1)
H_Backgrnd = cv2.imread("Horizon_Backgroung.png",-1)
Grnd_sky = cv2.imread("Horizon_GroundSky.png")

while True:
    Roll = cv2.getTrackbarPos('ROLL','CONTROLS')
    Pitch = cv2.getTrackbarPos('PITCH','CONTROLS')
    Sky = Grnd_sky[Pitch+197:Pitch+197+210,0:210].copy()
    #cv2.imshow('check1',H_Backgrnd[:,:,0])
    #cv2.imshow('check2',H_Backgrnd[:,:,3]/255.0)
    #cv2.imshow('check3',1.0 - H_Backgrnd[:,:,3]/255.0)
    #cv2.imshow('check3',H_Backgrnd[:,:,0]*H_Backgrnd[:,:,3]/255.0)
    for c in range(0,3):
        Sky[0:210,0:210, c] = H_Backgrnd[:,:,c] * (H_Backgrnd[:,:,3]/255.0) +  Sky[0:0+210, 0:210, c] * (1.0 - H_Backgrnd[:,:,3]/255.0)
    
    M = cv2.getRotationMatrix2D((210/2,210/2),Roll,1)
    Mark = cv2.warpAffine(Needle,M,(210,210))
    for c in range(0,3):
        Sky[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Sky[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)
    
    cv2.imshow('f',Sky)
    cv2.waitKey(1)

cv2.destroyAllWindows()
