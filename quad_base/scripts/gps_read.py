#!/usr/bin/python

import os
from gps import *
from time import *
import time
import threading

import rospy
import geometry_msgs.msg
from geometry_msgs.msg import Vector3
from std_msgs.msg import String
import std_msgs.msg

gpsd = None

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
 
    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
    gpsp = GpsPoller() # create the thread
    pub = rospy.Publisher('gps_talker', String, queue_size=10)
    rospy.init_node("gps_publisher", anonymous=True)
    rate = rospy.Rate(10)
    try:
        gpsp.start() # start it up
        while not rospy.is_shutdown():
            print
            print ' GPS reading'
            print '----------------------------------------'
            print 'latitude    ' , gpsd.fix.latitude
            print 'longitude   ' , gpsd.fix.longitude
 
            data = std_msgs.msg.String()
            data = str(gpsd.fix.latitude)+','+str(gpsd.fix.longitude)
            #data.x = 10.45
            #data.y = 78.45
            pub.publish(data)
            rate.sleep
            
    except rospy.ROSInterruptException: #when you press ctrl+c
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing
        pass
    print "Done.\nExiting."
    exit()
