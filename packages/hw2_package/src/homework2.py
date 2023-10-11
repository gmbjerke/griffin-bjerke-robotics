#!/usr/bin/python3

import rospy

from std_msgs.msg import String

def publisher():
	rospy.init_node('publisher', anonymous=True)
	pub = rospy.Publisher('chatter', String, queue_size=10)
	rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		data = "Hello world is this working please. %s" % rospy.get_time()
		rospy.loginfo(data)
		pub.publish(data)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		publisher()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
