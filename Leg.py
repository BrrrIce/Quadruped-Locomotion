# from Adafruit_Python_PCA9685 import PWM
from pygame.locals import *
# import RPi.GPIO as GPIO
import Resources as r
import Segment as s
import pygame
import time
import math
import sys
import os

# pwm = PWM(0x40)
# pwm.setPWMFreq(50)

offs_1 = 0
offs_2 = 0
offs_3 = 0

servo_min = 141 # Min pulse length out of 4096 150
servo_max = 932 # Max pulse length out of 4096  550

width = 1080
height = 720


class Leg():
	def __init__(self, screen, pos, id):
		self.leg_id = id
		self.objects = []
		self.segments = []
		
		self.screen = screen
		self.pos = pos
		self.spawn(2, 90, self.pos)
		
	def re_round(li, _prec=1):
		try:
			return round(li, _prec)
		except TypeError:
			return type(li)(re_round(x, _prec) for x in li)

	def update_list(self, _id, apos, bpos):
		self.id = int(_id)*2-2
		del self.segments[self.id:self.id+2]
		self.segments.insert(self.id,apos)
		self.segments.insert(self.id+1,bpos)
		
	def to360(self, deg):
		return str(round((deg+360)%360))[:-2]
		
	def get_local_angle(self, seg_id):
		self.s_angle = math.degrees(self.objects[seg_id-1].angle)
		if not seg_id == 1:
			self.s_angle -= math.degrees(self.objects[seg_id-2].angle)
		return self.to360(self.s_angle)
		
	def spawn(self, num, _length, pos):
		for i in range(0, num):
			self.objects.append(s.Segment(self.screen, i+1, _length, pos)) 
			self.update_list(i+1, self.objects[i].get_position()[0], self.objects[i].get_position()[1])

	def update(self, _end_eff, _angle):
		self.end_eff = (_end_eff[0]+self.pos[0], _end_eff[1]+self.pos[1])
			
		for item in reversed(self.objects):
			item.update(self.segments, self.end_eff)
			self.update_list(self.objects.index(item)+1, item.get_position()[0], item.get_position()[1])

		for item in self.objects:
			item.restrain(self.segments, self.get_local_angle(item.id), math.degrees(self.objects[item.id-2].angle))
			self.update_list(self.objects.index(item)+1, item.get_position()[0], item.get_position()[1])
			item.draw_line()
	
		### Rpi Implementation ###
	
		# self.servo0_angle = 180 - (self.objects[0].local_angle + 90 + offs_1 - 90)
		# self.servo1_angle = 180 - (self.objects[1].local_angle + 90 + offs_2)
		# self.servo2_angle = 180 - int(math.degrees(_angle))

			
		# self.pwm0_value = ((((servo_max-servo_min)*self.servo0_angle)/ 360) + servo_min)
		# self.pwm1_value = ((((servo_max-servo_min)*self.servo1_angle)/ 360) + servo_min)
		# self.pwm2_value = ((((servo_max-servo_min)*self.servo2_angle)/ 360) + servo_min)
		
		# if self.leg_id == 1:
			# pwm.setPWM(3,0,self.pwm0_value)
			# pwm.setPWM(4,0,self.pwm1_value)
			# pwm.setPWM(5,0,self.pwm2_value)
		# if self.leg_id == 2:
			# pwm.setPWM(0,0,self.pwm0_value)
			# pwm.setPWM(1,0,self.pwm1_value)
			# pwm.setPWM(2,0,self.pwm2_value)
		# if self.leg_id == 3:
			# pwm.setPWM(6,0,self.pwm0_value)
			# pwm.setPWM(7,0,self.pwm1_value)
			# pwm.setPWM(8,0,self.pwm2_value)
		# if self.leg_id == 4:
			# pwm.setPWM(9,0,self.pwm0_value)
			# pwm.setPWM(10,0,self.pwm1_value)
			# pwm.setPWM(11,0,self.pwm2_value)
