#!/usr/bin/python3
#Griffin Bjerke

import rospy
from std_msgs.msg import Float32, String
from odometry_hw.msg import Pose2D, DistWheel
import math

#rospy.set_param('/odom_ready', "ready")

class Odom:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.theta = 0
		self.pub = rospy.Publisher("/pose", Pose2D, queue_size=10)
		self.my2DPose = Pose2D(0,0,0)
		
		rospy.Subscriber("/dist_wheel", DistWheel, self.callback)
		
	def callback(self, disWheel):
		d_s = (disWheel.dist_wheel_left + disWheel.dist_wheel_right)/2
		d_theta = (disWheel.dist_wheel_right - disWheel.dist_wheel_left)/0.1
		d_x = d_s * math.cos(self.my2DPose.theta + d_theta/2)
		d_y = d_s * math.sin(self.my2DPose.theta + d_theta/2)
		self.my2DPose.x += d_x
		self.my2DPose.y += d_y
		self.my2DPose.theta += d_theta
		
		self.pub.publish(self.my2DPose)
		
if __name__ == '__main__':
	rospy.init_node('hw6')
	Odom()
	rospy.spin()
	
