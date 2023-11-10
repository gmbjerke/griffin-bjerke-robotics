#!/usr/bin/python3
#Griffin Bjerke
#11/9/2023
#HW7
#Fundamentals of Robotics Fall 2023

import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Hw7:
	def __init__(self):
		self.bridge = CvBridge()
		rospy.Subscriber("/image", Image, self.callback)
		
		
		# publish /image_cropped topic
		self.pub_cropped = rospy.Publisher("/image_cropped", Image, queue_size=10)
		
		# publish /image_white topic
		self.pub_white = rospy.Publisher("/image_white", Image, queue_size=10)
		
		# publish /image_yellow topic
		self.pub_yellow = rospy.Publisher("/image_yellow", Image, queue_size=10)
		
	def callback(self, msg):
		# converts ROS Image to CV Image
		cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
		
		# cropping 50%
		cv_cropped = cv_image[int(cv_image.shape[0]/2):cv_image.shape[0], 0:cv_image.shape[1]]
		
		# converts the image from BGR to HSV
		hsv_image = cv2.cvtColor(cv_cropped, cv2.COLOR_BGR2HSV)
		
		# converts image back to ROS Image
		ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped, "bgr8")
		
		# publish cropped image
		self.pub_cropped.publish(ros_cropped)
		
		# filter image for while lane markers
		filter_white = cv2.inRange(hsv_image, (0,0,225),(180,40,255))
		
		# convert white image to ROS Image
		ros_white = self.bridge.cv2_to_imgmsg(filter_white, "mono8")
		
		# publish white_filter
		self.pub_white.publish(ros_white)
		
		# filter image for yellow lane markers
		filter_yellow = cv2.inRange(hsv_image, (0,150,180),(70,255,255))
		
		# convert yellow image to ROS Image
		ros_yellow = self.bridge.cv2_to_imgmsg(filter_yellow, "mono8")
		
		# publish yellow filter
		self.pub_yellow.publish(ros_yellow)
		
if __name__ == "__main__":
	rospy.init_node("hw7")
	Hw7()
	rospy.spin()
	

