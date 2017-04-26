#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

class ImageConverter
{
  ros::NodeHandle n;
  image_transport::ImageTransport it;
  image_transport::Subscriber image_sub;
  image_transport::Publisher image_pub;
  
public:
  ImageConverter() 
   :it(n) //doubtful ask AJ 
  {
    image_sub = it.subscribe("/camera/rgb/image_raw", 1, &ImageConverter::imageCb,this);
    image_pub = it.advertise("/image_converter/output_video", 1); 
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

    cv::circle(cv_ptr->image, cv::Point(320, 240), 100, CV_RGB(255,0,0));
    cv::imshow("Image window", cv_ptr->image);
    cv::waitKey(3);
   
 image_pub.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
  ros::spin();
  cv::destroyWindow("Image window");

  return 0;
}
