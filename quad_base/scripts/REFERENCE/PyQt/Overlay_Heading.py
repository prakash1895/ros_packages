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
cv2.createTrackbar('YAW','CONTROLS',0,360,nothing)
Wheel = cv2.imread("HeadingWeel.png", -1)
Hea_Backgrnd = cv2.imread("HeadingIndicator_Background.png")
Hea_Backgrnd_copy = Hea_Backgrnd.copy()

while True:
    Yaw = cv2.getTrackbarPos('YAW','CONTROLS')
    M = cv2.getRotationMatrix2D((210/2,210/2),Yaw,1)
    Mark = cv2.warpAffine(Wheel,M,(210,210))
    for c in range(0,3):
        Hea_Backgrnd[0:210,0:210, c] = Mark[:,:,c] * (Mark[:,:,3]/255.0) +  Hea_Backgrnd[0:210, 0:210, c] * (1.0 - Mark[:,:,3]/255.0)

    cv2.imshow('f',Hea_Backgrnd)
    Hea_Backgrnd = Hea_Backgrnd_copy.copy()
    cv2.waitKey(1)

cv2.destroyAllWindows()
