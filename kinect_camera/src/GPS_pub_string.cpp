#include"ros/ros.h"
#include"std_msgs/String.h"
#include<sstream>
#include<unistd.h>
int main(int argc, char **argv)
{
	ros::init(argc, argv, "GPS_pub_string");
	ros::NodeHandle n;

	ros::Publisher pub_lat = n.advertise<std_msgs::String>("LatLng",1000);
	ros::Rate loop_rate(10);
	int count=1;

	while(ros::ok())
	{
		std_msgs::String msg_latlng;
		std::stringstream ss_latlng;
		
		if (count== 1)
			ss_latlng << "11.46,79.49";
		else if (count == 2)
			ss_latlng << "10.46,78.49";
		else if (count == 3)
			ss_latlng << "9.46,77.49";
		else if (count == 4)
			ss_latlng << "8.46,76.49";

		msg_latlng.data = ss_latlng.str();
		pub_lat.publish(msg_latlng);		
		usleep(5000000);
		
		count++;
		if (count == 5)
			count = 1;

		ros::spinOnce();
		loop_rate.sleep();
	}
	return 0;
}	
