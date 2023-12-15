#!/usr/bin/python3
#Griffin Bjerke
import sys
import rospy
from example_service.srv import Fibonacci, FibonacciResponse
import example_action_server.msg
import actionlib

class Hw10:
	def client(order):
		rospy.loginfo("Start Request")
		rospy.wait_for_service('/calc_fibonacci')
		try:
			s1 = rospy.ServiceProxy('/calc_fibonacci', Fibonacci)
			result = s1(order)
			rospy.loginfo(str(result))
			return result
		except rospy.ServiceException as error:
			print("Service Call Failed" + error)
			
	def client_action():
		client = actionlib.SimpleActionClient('/fibonacci', example_action_server.msg.FibonacciAction)
		client.wait_for_server()
		
		rospy.loginfo("Order 1 sent")
		order1 = example_action_server.msg.FibonacciGoal(3)
		client.send_goal(order1)
		client.wait_for_result()
		rospy.loginfo("Action Sequence: " + str(client.get_result()))
		
		rospy.loginfo("Order 2 sent")
		order2 = example_action_server.msg.FibonacciGoal(15)
		client.send_goal(order2)
		client.wait_for_result()
		rospy.loginfo("Action Sequence: " + str(client.get_result()))
		
		rospy.loginfo("ORDERS COMPLETED")
		
	if __name__ == '__main__':
		rospy.init_node('hw10')
		
		client(3)
		client(15)
		client_action()
