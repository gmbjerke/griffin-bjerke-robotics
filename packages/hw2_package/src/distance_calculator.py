#!/usr/bin/python3

import rospy
from turtlesim.msg import Pose
from turtlesim_helper.msg import UnitsLabelled
import math

class DistanceCalculator:
	def __init__(self):
		self.distance = 0
		self.prev_x = 0
		self.prev_y = 0
		self.distance_msg = UnitsLabelled()
		self.distance_msg.units = "meters"
		rospy.Subscriber('/turtle1/pose', Pose, self.pose_callback)
		self.distance_units = rospy.Publisher('distance_traveled', UnitsLabelled, queue_size=10)
		self.distance_units.publish(self.distance_msg)
		
	def pose_callback(self, data):
		self.distance = ((data.x - self.prev_x)**2 + (data.y - self.prev_y)**2)**0.5
		self.prev_x = data.x
		self.prev_y = data.y
		
		self.distance_msg.value += self.distance
		self.distance_units.publish(self.distance_msg)
		
if __name__ == '__main__':
	rospy.init_node('DistanceCalculator')
	DistanceCalculator()
	rospy.spin()
