from Adafruit_PWM_Servo_Driver import PWM
from pygame.locals import *
import RPi.GPIO as GPIO
import Resources as r
import Segment as s
import pygame
import time
import math
import sys
import os

pwm = PWM(0x40)
pwm.setPWMFreq(50)

offs_1 = 0
offs_2 = 0
offs_3 = 0

servo_min = 141 # Min pulse length out of 4096 
servo_max = 932 # Max pulse length out of 4096  

width = 1080
height = 720

pygame.init
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])

objects = []
segments = []
	
def re_round(li, _prec=1):
	try:
		return round(li, _prec)
	except TypeError:
		return type(li)(re_round(x, _prec) for x in li)

def update_list(_id, apos, bpos):
	id = int(_id)*2-2
	del segments[id:id+2]
	segments.insert(id,apos)
	segments.insert(id+1,bpos)
	
def to360(deg):
	return str(round((deg+360)%360))[:-2]
	
def get_local_angle(seg_id):
	s_angle = math.degrees(objects[seg_id-1].angle)
	if not seg_id == 1:
		s_angle -= math.degrees(objects[seg_id-2].angle)
	return to360(s_angle)
	
def spawn(num, _length, pos):
	for i in range(0, num):
		objects.append(s.Segment(screen, i+1, _length, pos)) 
		update_list(i+1, objects[i].get_position()[0], objects[i].get_position()[1])

def get_end_effectors():	
	for i in range(0,4):
		angle = math.atan2(local_poss[i][1]+320*.3, local_poss[i][0][0]*2)
		x1 = local_poss[i][0][1]*2
		y1 = math.hypot(abs(local_poss[i][0][0]*2), local_poss[i][1])
		end_effs[i] = [[x1*-1, y1], angle]
		
def update_screen():
	pygame.display.update()

		
spawn(2, 90, (width/2,height/2))

leg_id = 1	
running = True		
while running:
	clock.tick(60)
	mouse_pos = pygame.mouse.get_pos()
	screen.fill(r.white)

	end_eff = mouse_pos
	_angle = math.pi / 2
	
		
	for item in reversed(objects):
		item.update(segments, end_eff)
		update_list(objects.index(item)+1, item.get_position()[0], item.get_position()[1])

	for item in objects:
		item.restrain(segments, get_local_angle(item.id), math.degrees(objects[item.id-2].angle))
		update_list(objects.index(item)+1, item.get_position()[0], item.get_position()[1])
		item.draw_line()

	servo0_angle = 180 - (objects[0].local_angle + 90 + offs_1 - 90)
	servo1_angle = 180 - (objects[1].local_angle + 90 + offs_2)
	servo2_angle = 180 - int(math.degrees(_angle))

		
	pwm0_value = ((((servo_max-servo_min)*servo0_angle)/ 360) + servo_min)
	pwm1_value = ((((servo_max-servo_min)*servo1_angle)/ 360) + servo_min)
	pwm2_value = ((((servo_max-servo_min)*servo2_angle)/ 360) + servo_min)
	
	if leg_id == 1:
		pwm.setPWM(3,0,pwm0_value)
		pwm.setPWM(4,0,pwm1_value)
		pwm.setPWM(5,0,pwm2_value)
	if leg_id == 2:
		pwm.setPWM(0,0,pwm0_value)
		pwm.setPWM(1,0,pwm1_value)
		pwm.setPWM(2,0,pwm2_value)
	if leg_id == 3:
		pwm.setPWM(6,0,pwm0_value)
		pwm.setPWM(7,0,pwm1_value)
		pwm.setPWM(8,0,pwm2_value)
	if leg_id == 4:
		pwm.setPWM(9,0,pwm0_value)
		pwm.setPWM(10,0,pwm1_value)
		pwm.setPWM(11,0,pwm2_value)

	update_screen()
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pwm.setPWM(0,0,0)
			pwm.setPWM(1,0,0)
			pwm.setPWM(2,0,0)
			pwm.setPWM(3,0,0)
			pwm.setPWM(4,0,0)
			pwm.setPWM(5,0,0)
			pwm.setPWM(6,0,0)
			pwm.setPWM(7,0,0)
			pwm.setPWM(8,0,0)
			pwm.setPWM(9,0,0)
			pwm.setPWM(10,0,0)
			pwm.setPWM(11,0,0)
			running = False
			pygame.quit()
		if i.type == KEYDOWN:
			if i.key == K_f:
				leg_id += 1
				if leg_id == 5:
					leg_id = 1
		