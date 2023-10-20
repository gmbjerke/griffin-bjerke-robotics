#!/usr/bin/python3

from turtle import speed
import rospy
from geometry_msgs.msg import Twist
import math
import time
 
def move_sq():
	rospy.init_node('move_sq', anonymous=True)
	vel_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()
	i = 0
	time.sleep(3)
	while i <= 20:
		speed  = 0.75
		angle = 110
		distance = 2
		
		vel_msg.linear.x = speed
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0
		
		t0 = rospy.Time.now().to_sec()
		current_distance = 0
		
		while(current_distance <= distance):
			vel_pub.publish(vel_msg)
			t1 = rospy.Time.now().to_sec()
			current_distance = speed*(t1-t0)
		
		vel_msg.linear.x = 0
		vel_pub.publish(vel_msg)
		angular_speed = 2
		vel_msg.angular.z = (angular_speed)
		current_angle = 0
		
		t0 = rospy.Time.now().to_sec()
		while(current_angle <= math.pi/2.0):
			vel_pub.publish(vel_msg)
			t1 = rospy.Time.now().to_sec()
			current_angle = angular_speed*(t1-t0)
		
		i += 1
		vel_msg.angular.z = 0
		vel_pub.publish(vel_msg)
		
if __name__ == '__main__':
	try:
		move_sq()
	except rospy.ROSInterruptException:
		pass
