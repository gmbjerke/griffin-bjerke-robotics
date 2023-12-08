#!/usr/bin/python3
# Griffin Bjerke

import rospy
from std_msgs.msg import Float32, String
from pid import PID

class Hw9:
	def __init__(self):
		# publishers
		self.pub = rospy.Publisher("/control_input", Float32, queue_size=10)
		self.get_pid = PID(p=0.00008, i=0.025, d=0.5)
		
		rospy.set_param("controller_ready", "ready")
		
		rospy.Subscriber("/error", Float32, self.callback)
		
	def callback(self, error):
		# publish to pid controller
		result = self.get_pid.feedback_control(error.data, 0.007)
		self.pub.publish(result)
		
if __name__ == '__main__':
	rospy.init_node('hw9')
	rospy.sleep(3)
	Hw9()
	rospy.spin()
