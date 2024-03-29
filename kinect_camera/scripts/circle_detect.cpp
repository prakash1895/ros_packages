#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <stdio.h>

class circle_detect
{
  ros::NodeHandle n;
  image_transport::ImageTransport it;
  image_transport::Subscriber image_sub;
  image_transport::Publisher image_pub;
  
public:
  circle_detect() 
   :it(n) 
  {
    image_sub = it.subscribe("/usb_cam/image_raw", 1, &circle_detect::imageCb,this); //change the subscription topic
    image_pub = it.advertise("/image_converter/output_video", 1); 
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
	using namespace cv;
    cv_bridge::CvImagePtr cv_ptr;
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

    	Mat src_gray;
	cvtColor( cv_ptr->image, src_gray, CV_BGR2GRAY );
	GaussianBlur( src_gray, src_gray, Size(9, 9), 2, 2 );
	vector<Vec3f> circles;
	HoughCircles( src_gray, circles, CV_HOUGH_GRADIENT, 1, src_gray.rows/8, 100, 20, 0, 0 );

	for( size_t i = 0; i < circles.size(); i++ )
 	 {
      	   Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
      	   int radius = cvRound(circles[i][2]);
      	   circle( cv_ptr->image, center, radius,CV_RGB(0,0,255)); // circle outliner
  	 }

    imshow("Image window", cv_ptr->image);
    waitKey(1);
   
 image_pub.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "circle_detect");
  circle_detect ic;
  ros::spin();
  cv::destroyWindow("Image window");

  return 0;
}


