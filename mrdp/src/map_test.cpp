#include<ros/ros.h>
#include<geometry_msgs/PoseArray.h>
#include<std_msgs/Float64.h>
#include<geometry_msgs/Vector3.h>
class map_test
{

public:
	map_test();
	//void GPS_pub();
private:
	ros::NodeHandle n;
	ros::Publisher pub;
	
};
/*
void map_test::GPS_pub()
{
	
	geometry_msgs::Vector3 GPS; 	
	GPS.x = 10.7123;
	GPS.y = 82.3416;
	GPS.z = 0.000;
	pub.publish(GPS);
			
}
*/
map_test::map_test()
{
	pub = n.advertise<geometry_msgs::Vector3>("/GPS_testing",100);
	geometry_msgs::Vector3 GPS; 	
	GPS.x = 10.7123;
	GPS.y = 82.3416;
	GPS.z = 0.000;
	pub.publish(GPS);
	
	
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "map_test");
map_test k;
ros::spin();
}

