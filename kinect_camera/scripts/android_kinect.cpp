#include<ros/ros.h>
#include<geometry_msgs/Vector3.h>
#include<std_msgs/Float64.h>

class android_kinect
{

public:
	android_kinect();
private:
	ros::NodeHandle n;
	ros::Publisher pub;
	ros::Subscriber sub;
	void callback(const geometry_msgs::Vector3::ConstPtr& num);
};

void android_kinect::callback (const geometry_msgs::Vector3::ConstPtr& num)
{
	std_msgs::Float64 tilt;
	tilt.data = (num->x);
	pub.publish(tilt);
}

android_kinect::android_kinect()
{
	
	sub = n.subscribe<geometry_msgs::Vector3>("/Orientation", 1000, &android_kinect::callback,this);
	pub = n.advertise<std_msgs::Float64>("/tilt_angle",1000);
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "android_kinect");
android_kinect k;
ros::spin();
}
