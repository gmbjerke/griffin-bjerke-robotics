#!/usr/bin/python3
# Griffin Bjerke

from std_msgs.msg import Float32, String

class PID:
	def __init__(self, p, i, d):
		self.kp = p
		self.ki = i
		self.kd = d
		self.prev_err = 0
		self.i = 0
		
	def feedback_control(self, error, dt):
		p = error
		self.i += (error * dt)
		d = (error - self.prev_err) / dt
		self.prev_err = error
		
		pid_controller = (self.kp * p) + (self.ki * self.i) + (self.kd * d)
		return pid_controller
	
