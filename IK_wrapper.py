from Adafruit_PWM_Servo_Driver import PWM
from pygame.locals import *
import Resources as r
import Leg as l
import pygame
import random as ra
import math
import time

# time.sleep(4)



pwm = PWM(0x40)
pwm.setPWMFreq(50)

width = 1080
height = 720

pygame.init
pygame.joystick.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])

joystick = pygame.joystick.Joystick(0)
joystick.init()

legs = []
feet = [[0,0],[0,0],[0,0],[0,0]]
local_poss = [[[0,0],185],[[0,0],185],[[0,0],185],[[0,0],185]]
end_effs = [[[0,0],0],[[0,0],0],[[0,0],0],[[0,0],0]]
guides = [[100, 0],[100, 0],[100, 0],[100, 0]]  # magnitude, angle

def update_screen():
	pygame.display.update()

def draw_rect(pos, size, color):
	top_left = (pos[0]-(size[0]/2) , pos[1]-(size[1]/2))
	pygame.draw.rect(screen, color, [top_left,size], 5)

def draw_foot(id, pos, size, sel):
	if sel == 1:
		pygame.draw.circle(screen, r.green, (int(pos[0]),int(pos[1])), size)
	elif sel == 2:
		pygame.draw.circle(screen, r.black, (int(pos[0]),int(pos[1])), size)
	elif sel == 3:
		pygame.draw.circle(screen, r.red, (int(pos[0]),int(pos[1])), size)
		
def get_guide_pos(id):
	mag = guides[id][0]
	angle = guides[id][1]
	
	ang = math.radians(angle) - (math.pi/2)
	top_guide = (math.cos(ang)*(mag/2), math.sin(ang)*(mag/2))
	bottom_guide = (math.cos(ang)*((mag/2)*-1), math.sin(ang)*((mag/2)*-1))
	return (top_guide, bottom_guide)

def set_on_guide(id, pe):
	angle = guides[id][1]
	ang = math.radians(angle - 90)
	local_poss[id][0] = [math.cos(ang)*(pe), math.sin(ang)*(pe)]
	
def get_stride_depth(id, depth):
	mag = guides[id][0]
	x = math.sqrt(local_poss[id][0][0]**2 + local_poss[id][0][1]**2)
	y = (x*depth) / (mag/2)
	return y

		
def draw_overhead_view(pos, size, sel):
	draw_rect(pos,size, r.green)
	body_size = [size[0]*.4,size[1]*.5]
	draw_rect(pos,body_size, r.blue)
	
	for id in range(0,4):
		if id == 0:
			leg = [pos[0]+body_size[0]/2,pos[1]-body_size[1]/2]
		if id == 1:
			leg = [pos[0]-body_size[0]/2,pos[1]-body_size[1]/2]
		if id == 2:
			leg = [pos[0]-body_size[0]/2,pos[1]+body_size[1]/2]
		if id == 3:
			leg = [pos[0]+body_size[0]/2,pos[1]+body_size[1]/2]
		
		feet[id] = [leg[0]+local_poss[id][0][0], leg[1]+local_poss[id][0][1]]
		draw_foot(1, (get_guide_pos(id)[0][0]+leg[0], get_guide_pos(id)[0][1]+leg[1]), 8, 3)
		draw_foot(1, (get_guide_pos(id)[1][0]+leg[0], get_guide_pos(id)[1][1]+leg[1]), 8, 3)
		if sel == (id+1):
			draw_foot(1, feet[id], 8, 1)
		else:
			draw_foot(1, feet[id], 8, 2)
			
def get_end_effectors():	
	for i in range(0,4):
		angle = math.atan2(local_poss[i][1]+320*.3, local_poss[i][0][0]*2)
		x1 = local_poss[i][0][1]*2
		y1 = math.hypot(abs(local_poss[i][0][0]*2), local_poss[i][1])
		end_effs[i] = [[x1*-1, y1], angle]
	
def spawn_leg(pos, id):
	legs.append(l.Leg(screen, pos, id))

guides[0][1] = 180
guides[2][1] = 180

spawn_leg([850,400], 1)
spawn_leg([850,200], 2)
spawn_leg([600,200], 3)
spawn_leg([600,400], 4)

step_height = 100
step_scale = 17
base_height = 160
walk_speed = .18

test = 0
z = 0
curr_foot = 1
running = True
while running:
	clock.tick(60)
	screen.fill(r.white)
	
	axis2 = joystick.get_axis(2)
	axis3 = joystick.get_axis(3)
	step_scale = math.sqrt(axis2**2 + axis3**2)*-17
	
	guides[0][1] = 180 - math.degrees(math.atan2(axis2, axis3))
	guides[1][1] = 180 - math.degrees(math.atan2(axis2, axis3)) + 180
	guides[2][1] = 180 - math.degrees(math.atan2(axis2, axis3))
	guides[3][1] = 180 - math.degrees(math.atan2(axis2, axis3)) + 180
	
	test = math.cos(z)
	z  += walk_speed
	if math.cos(z) > test:
		sign = "+"
	else:
		sign = "-"
	
	set_on_guide(0, math.cos(z)*step_scale)
	if sign == "-":
		local_poss[0][1] = get_stride_depth(0, step_height) + base_height

	set_on_guide(1, math.cos(z)*step_scale)
	if sign == "+":
		local_poss[1][1] = get_stride_depth(1, step_height) + base_height
		
	set_on_guide(2, math.cos(z)*step_scale)
	if sign == "-":
		local_poss[2][1] = get_stride_depth(2, step_height) + base_height
		
	set_on_guide(3, math.cos(z)*step_scale)
	if sign == "+":
		local_poss[3][1] = get_stride_depth(3, step_height) + base_height
	

	
	draw_overhead_view([160,160],[320,320], curr_foot)
	get_end_effectors()
	
	for item in legs:
		item.update(end_effs[item.leg_id-1][0], end_effs[item.leg_id-1][1])

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
				for j in range(0,4):
					guides[j][1] -=12
			if i.key == K_g:
				for j in range(0,4):
					guides[j][1] +=12
			
			if i.key == K_q:
				step_scale -=1
				print step_scale
			if i.key == K_w:
				step_scale +=1
				print step_scale
				
			if i.key == K_c:
				curr_foot += 1
				if curr_foot == 6:
					curr_foot = 1

			if i.key == K_UP and curr_foot != 5:
				local_poss[curr_foot-1][0][1] -= 6
			if i.key == K_DOWN and curr_foot != 5:
				local_poss[curr_foot-1][0][1] += 6
			if i.key == K_LEFT and curr_foot != 5:
				local_poss[curr_foot-1][0][0] -= 6
			if i.key == K_RIGHT and curr_foot != 5:
				local_poss[curr_foot-1][0][0] += 6
