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
cv2.createTrackbar('YAW','CONTROLS',0,50,nothing)
Ball = cv2.imread("TurnCoordinatorBall.png", -1)
T_Backgrnd = cv2.imread("Turn_Background.png")
T_Backgrnd_copy = T_Backgrnd.copy()

while True:
    Yaw = cv2.getTrackbarPos('YAW','CONTROLS')
    for c in range(0,3):
        T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] =  Ball[:,:,c] * (Ball[:,:,3]/255.0) +  T_Backgrnd[19:19+14, 98+Yaw:98+Yaw+14, c] * (1.0 - Ball[:,:,3]/255.0)

    cv2.imshow('f',T_Backgrnd)
    T_Backgrnd = T_Backgrnd_copy.copy()
    cv2.waitKey(1)

cv2.destroyAllWindows()
