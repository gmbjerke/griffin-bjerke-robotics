#!/usr/bin/python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import message_filters
import numpy as np

class Hw8:
	def __init__(self):
		self.bridge = CvBridge()
		# create subscribers
		self.sub_cropped = message_filters.Subscriber("image_cropped", Image)
		self.sub_yellow = message_filters.Subscriber("image_yellow", Image)
		self.sub_white = message_filters.Subscriber("image_white", Image)
		
		# timeSynchronizer
		self.ts = message_filters.TimeSynchronizer([self.sub_cropped, self.sub_yellow, self.sub_white], 10)
		self.ts.registerCallback(self.callback)
		# create publishers
		self.pub_canny = rospy.Publisher("/image_canny", Image, queue_size=10)
		self.pub_yellow = rospy.Publisher("/image_lines_yellow", Image, queue_size=10)
		self.pub_white = rospy.Publisher("/image_lines_white", Image, queue_size=10)
		self.pub_lines_all = rospy.Publisher("/image_lines_all", Image, queue_size=10)
		
	def callback(self, cropped_msg, yellow_msg, white_msg):
		
		# convert image so it can be used by OpenCV
		cv_cropped = self.bridge.imgmsg_to_cv2(cropped_msg, "bgr8")
		cv_yellow = self.bridge.imgmsg_to_cv2(yellow_msg, "mono8")
		cv_white = self.bridge.imgmsg_to_cv2(white_msg, "mono8")
		
		# edge detection
		edges = cv2.Canny(cv_cropped, 0, 255)
		
		# convert OpenCV image back to ROS
		canny = self.bridge.cv2_to_imgmsg(edges, "mono8")
		self.pub_canny.publish(canny)
		
		# dilate
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
		kernel_edges = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,1))
		dilated_yellow = cv2.dilate(cv_yellow, kernel)
		dilated_white = cv2.dilate(cv_white, kernel)
		dilated_edges = cv2.dilate(edges, kernel_edges)
		
		
		and_yellow = cv2.bitwise_and(dilated_edges, dilated_yellow, mask=None)
		and_white = cv2.bitwise_and(dilated_edges, dilated_white, mask=None)
		
		# Hough transformation
		hough_yellow = cv2.HoughLinesP(and_yellow, 1, np.pi/180, 5, None, 3, 2)
		hough_white = cv2.HoughLinesP(and_white, 1, np.pi/180, 5, None, 10, 5)
		
		# draw output lines
		image_lines_yellow = self.output_lines(cv_cropped, hough_yellow)
		image_lines_white = self.output_lines(cv_cropped, hough_white)

		# combine yellow and white lines
		image_lines_all = cv2.addWeighted(image_lines_yellow, 0.5, image_lines_white, 0.5, 0)

		# convert remaining images to ROS to be published
		ros_yellow = self.bridge.cv2_to_imgmsg(image_lines_yellow, "bgr8")
		ros_white = self.bridge.cv2_to_imgmsg(image_lines_white, "bgr8")
		ros_lines_all = self.bridge.cv2_to_imgmsg(image_lines_all, "bgr8")
		
		self.pub_yellow.publish(ros_yellow)
		self.pub_white.publish(ros_white)
		self.pub_lines_all.publish(ros_lines_all)
		
	def output_lines(self, original_image, lines):
		output = np.copy(original_image)
		if lines is not None:
			for i in range(len(lines)):
				l = lines[i][0]
				cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
				cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
				cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
		return output
		
if __name__=="__main__":
	rospy.init_node("hw8")
	Hw8()
	rospy.spin()
	
				
