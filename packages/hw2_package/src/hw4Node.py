#!/usr/bin/python3

import rospy
from turtlesim_helper.msg import UnitsLabelled

class hw4_param:
	def __init__(self):
		self.msg = UnitsLabelled()
		self.msg.units = "smoots"
		rospy.Subscriber("/distance_traveled", UnitsLabelled, self.callback)
		self.units = rospy.Publisher("/output1", UnitsLabelled, queue_size=10)
		
	def callback(self,msg):
		if rospy.has_param("/distance_converter"):
			self.unit = rospy.get_param("/distance_converter")
		else:
			self.unit = "smoots"
			
		if (self.unit == "meters"):
			self.msg.value = msg.value
			slef.units.publish(self.msg)
		elif (self.unit == "feet"):
			self.msg.value = msg.value*3.28084
			self.units.publish(self.msg)
		else:
			self.msg.value = msg.value*1.7018
			self.units.publish(self.msg)
			
if __name__== '__main__':
	rospy.init_node('hw4_param')
	hw4_param()
	rospy.spin()
