#include <ros/ros.h>
#include <string>
#include <geometry_msgs/PoseArray.h>
#include <sensor_msgs/JointState.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/Vector3.h>
#include <stdlib.h>
#include <math.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Twist.h>


class GPS
{
public:
	GPS(); 
        void GPS_pub_function();  
private:
	ros::NodeHandle n; 
	ros::Publisher GPS_pub; 
					
};

void GPS::GPS_pub_function()
{
geometry_msgs::Twist GPS;
GPS.linear.x = 7.5;
GPS.linear.y = 7.5;
GPS.linear.z = 7.5; 
GPS.angular.z = 12.0;
GPS_pub.publish(GPS);
}

GPS::GPS() //constructor
{

	GPS_pub = n.advertise<geometry_msgs::Twist>("/Quad_vel_manual",100); 
        
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "GPS");
GPS k;
while(ros::ok())
{
k.GPS_pub_function();
}
ros::spin();
}

