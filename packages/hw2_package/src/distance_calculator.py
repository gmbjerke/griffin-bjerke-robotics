#!/usr/bin/python3

import rospy
from turtlesim.msg import Pose
from turtlesim_helper.msg import UnitsLabelled

class DistanceCalculator:
	def __init__(self):
		rospy.init_node('distance_calculator')
		
		self.distance_pub = rospy.Publisher('distance_traveled', UnitsLabelled, queue_size=10)
		self.prev_pose = None
		
		rospy.Subscriber('turtle1/pose', Pose, self.pose_callback)
		
	def pose_callback(self, data):
		if self.prev_pose is not None:
			distance = ((data.x - self.prev_pose.x)**2 + (data.y - self.prev_pose.y)**2)**0.5
			
			distance_msg = UnitsLabelled()
			distance_msg.value = distance
			distance_msg.units = "meters"
			self.distance_pub.publish(distance_msg)
			
			self.prev_pose = data
		
if __name__ == '__main__':
	try:
		dc = DistanceCalculator()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
