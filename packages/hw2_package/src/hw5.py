#!/usr/bin/python3

import rospy
import numpy as np
from duckietown_msgs.msg import Vector2D

class hw5:
	def __init__(self):
		rospy.Subscriber("/sensor_coord", Vector2D, self.callback)
		self.pub_robot = rospy.Publisher("/robot_coord", Vector2D, queue_size = 10)
		self.pub_world = rospy.Publisher("/world_coord", Vector2D, queue_size = 10)
		self.pub_msg = Vector2D()
		
		robotx = 10
		roboty = 5
		sensorx = -1
		sensory = 0
		robotangle = 135
		sensorangle = 180
		rRs = np.array([[np.cos(sensorangle*np.pi/180), -1*np.sin(sensorangle*np.pi/180)], [np.sin(sensorangle*np.pi/180), np.cos(sensorangle*np.pi/180)]])
		rPs = np.array([[sensorx],[sensory]])
		row_L = np.array([0,0,1])
		rTs = np.concatenate((rRs, rPs), axis = 1)
		
		self.rTs = np.vstack([rTs, row_L])
		wRr = np.array([[np.cos(robotangle*np.pi/180), -1*np.sin(robotangle*np.pi/180)], [np.sin(robotangle*np.pi/180), np.cos(robotangle*np.pi/180)]])
		wPr = np.array([[robotx],[roboty]])
		wTr = np.concatenate((wRr, wPr), axis = 1)
		self.wTr = np.vstack([wTr, row_L])
		
	def callback(self,msg):
		obstacle_sensor = np.array([[msg.x], [msg.y], [1]])
		obstacle_robot = np.matmul(self.rTs, obstacle_sensor)
		self.pub_msg.x = obstacle_robot.item((0,0))
		self.pub_msg.y = obstacle_robot.item((1,0))
		self.pub_robot.publish(self.pub_msg)
		obstacle_world = np.matmul(self.wTr, obstacle_robot)
		self.pub_msg.x = obstacle_world.item((0,0))
		self.pub_msg.y = obstacle_world.item((1,0))
		self.pub_world.publish(self.pub_msg)
		
if __name__ == '__main__':
	rospy.init_node('hw5')
	hw5()
	pub_sensor = rospy.Publisher("/sensor_coord", Vector2D, queue_size=10)
	
	obstacle1 = Vector2D(x=3,y=2)
	obstacle2 = Vector2D(x=7,y=-6)
	obstacle3 = Vector2D(x=-12,y=5)
	obstacle4 = Vector2D(x=-6,y=-6)
	
	rate = rospy.Rate(1)
	
	while not rospy.is_shutdown():
		pub_sensor.publish(obstacle1)
		pub_sensor.publish(obstacle2)
		pub_sensor.publish(obstacle3)
		pub_sensor.publish(obstacle4)
		rate.sleep()

	rospy.spin()

