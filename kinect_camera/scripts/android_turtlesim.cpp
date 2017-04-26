#include<ros/ros.h>
#include<std_msgs/Int16.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Vector3.h>

class arduino_turtlesim
{
public:
	arduino_turtlesim();
private:
	ros::NodeHandle n;
	ros::Publisher pub;
	ros::Subscriber sub;
	//void callback(const std_msgs::Int16::ConstPtr& num);
	void callback(const geometry_msgs::Vector3::ConstPtr& num);

};

//void arduino_turtlesim::callback (const std_msgs::Int16::ConstPtr& num)
void arduino_turtlesim::callback (const geometry_msgs::Vector3::ConstPtr& num)
{
/*
	geometry_msgs::Twist vel;
	if (num->data == (1))
	{
		vel.linear.x  = 3;
		vel.angular.z = 1;
	}
	else
	{
		vel.linear.x = 5;
		vel.angular.z = -4;
	}

*/
	geometry_msgs::Twist vel;
	vel.linear.x = (num->y); 
	vel.angular.z = (num->x);
	pub.publish(vel);
}

arduino_turtlesim::arduino_turtlesim()
{
	
	sub = n.subscribe<geometry_msgs::Vector3>("/chatter", 1000, &arduino_turtlesim::callback,this);
	pub = n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",1000);
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "arduino_turtlesim");
arduino_turtlesim k;
ros::spin();
}
