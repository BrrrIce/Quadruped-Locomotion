import pygame
import Resources as r
import math as m

width = 1080
height = 720


class Segment():	

	def __init__(self, _screen, _id, _length, _start_pos):
		self.screen = _screen
		self.id = _id
		self.length = _length
		self.a = (0,0)
		self.b = (0,0)
		self.start_pos = _start_pos
		if self.id == 1:
			self.length = 320*.41
		elif self.id == 2:
			self.length = 320*.3
		
		
	def to360(self, deg):
		return str(round((deg+360)%360))[:-2]
		
	def get_global_angle(self, _pos1, _pos2):
		self.pos_1 = _pos1
		self.pos_2 = _pos2
		return m.atan2(self.pos_2[1]-self.pos_1[1],self.pos_2[0]-self.pos_1[0])

	def restrain(self, _segments, _local_angle, _prev_angle):
		self.segments = _segments
		self.local_angle = int(_local_angle)-180 # local angle retrieved correctly
		self.prev_angle = int(_prev_angle) # previous angle retrieved correctly
		if self.id == 1:
			self.a = self.start_pos
			self.angle = self.get_global_angle(self.a, self.b)
			self.b = (m.cos(self.angle)*self.length+self.a[0], m.sin(self.angle)*self.length+self.a[1])
		else:
			self.g_angle = self.prev_angle+self.local_angle # global angle calculated correctly
			self.a = self.segments[(self.id*2-2)-1]
			self.angle = self.get_global_angle(self.a, self.b)
			self.b = (m.cos(self.angle)*self.length+self.a[0], m.sin(self.angle)*self.length+self.a[1])
			
	def update(self, _segments, end_eff):
		self.segments = _segments
		# mouse_pos = pygame.mouse.get_pos()

		if self.id == len(self.segments)/2:
			self.b = end_eff
			self.angle = self.get_global_angle(self.b, self.a)
			self.a = (m.cos(self.angle)*self.length+self.b[0], m.sin(self.angle)*self.length+self.b[1])
		else:
			self.b = self.segments[(self.id*2-2)+2]
			self.angle = self.get_global_angle(self.b, self.a)
			self.a = (m.cos(self.angle)*self.length+self.b[0], m.sin(self.angle)*self.length+self.b[1])
				
	def draw_line(self):
		pygame.draw.line(self.screen, r.black, self.a, self.b, 4)

	def get_position(self):
		return (self.a, self.b)