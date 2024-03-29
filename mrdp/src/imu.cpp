#include<ros/ros.h>
#include<geometry_msgs/PoseArray.h>
#include<std_msgs/Float64.h>
#include<geometry_msgs/Vector3.h>
class imu
{

public:
	imu();
private:
	ros::NodeHandle n;
	ros::Subscriber sub;
	ros::Publisher pub;
	void callback(const geometry_msgs::Vector3::ConstPtr& imu);
};

void imu::callback (const geometry_msgs::Vector3::ConstPtr& imu)
{
	std_msgs::Float64 x; 	
	x.data = (imu->x);
	pub.publish(x);
			
}

imu::imu()
{
	
	sub = n.subscribe<geometry_msgs::Vector3>("/arduino_acc", 100, &imu::callback,this);
	pub = n.advertise<std_msgs::Float64>("/echoo",100);
	
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "imu");
imu k;
ros::spin();
}
