import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from template_sample import Ui_Form
import cv2
import numpy as np

flag = 0
app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)

def display():
    img = cv2.imread("/home/adisorn/catkin_ws/src/beginner_tutorials/scripts/Cloudrone/2.JPG")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(img,(500,500))
    ui.Frame.setPixmap(QPixmap(QtGui.QImage(frame,frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)))
    window.show()
    cv2.waitKey(1)
    
def done():
    global flag
    flag ==1
    cv2.destroyAllWindows()
    sys.exit(app.exec_())
    
while flag == 0:
    ui.button.clicked.connect(done)
    display()
   
     
