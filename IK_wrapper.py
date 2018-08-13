from pygame.locals import *
import Resources as r
import Leg as l
import pygame
import random as ra
import math
import time


width = 1080
height = 720

pygame.init
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])

walk_gait = [
	[[0,25],[45,100]],    # leg1
	[[0,5],[20,100]],     # leg2
	[[0,50],[70,100]], 	  # leg3
	[[0,75],[95,100]], 	  # leg4
	]

trot_gait = [
	[0, 60],              # leg1
	[[0,10],[50, 100]],	  # leg2
	[0, 60],			  # leg3
	[[0,10],[50,100]]	  # leg4
	]

legs = []
feet = [[0,0],[0,0],[0,0],[0,0]]
local_poss = [[[0,0],185],[[0,0],185],[[0,0],185],[[0,0],185]]
end_effs = [[[0,0],0],[[0,0],0],[[0,0],0],[[0,0],0]]
guides = [[100, 0],[100, 0],[100, 0],[100, 0]]  # magnitude, angle

def update_screen():
	pygame.display.update()

def draw_rect(pos, size, color, s):
	top_left = (pos[0]-(size[0]/2) , pos[1]-(size[1]/2))
	pygame.draw.rect(screen, color, [top_left,size], s)
	
def draw_line(x, y, c, s):
	pygame.draw.line(screen, c, x, y, s)

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
	local_poss[id][0] = [math.cos(ang)*pe, math.sin(ang)*pe]
	
def draw_overhead_view(pos, size, sel):
	draw_rect(pos,size, r.green, 5)
	body_size = [size[0]*.4,size[1]*.5]
	draw_rect(pos,body_size, r.blue, 5)
	
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
	for i in range(4):
		angle = math.atan2(local_poss[i][1]+320*.3, local_poss[i][0][0]*2)
		x1 = local_poss[i][0][1]*2
		y1 = math.hypot(abs(local_poss[i][0][0]*2), local_poss[i][1])
		end_effs[i] = [[x1*-1, y1], angle]
	
def spawn_leg(pos, id):
	legs.append(l.Leg(screen, pos, id))

def move_legs(_tick, base_height, step_height, speed, step_len, gait):
	tick = _tick
	for i in range(4):
		try:
			test = gait[i][0][0]
			if (tick > gait[i][0][0] and tick < gait[i][0][1]) or (tick > gait[i][1][0] and tick < gait[i][1][1]):
				if local_poss[i][1] <= base_height:
					local_poss[i][1] += speed
				
				if  tick > gait[i][1][0] and tick < gait[i][1][1]:
					l_tick = tick - gait[i][1][0]
					s_tick = (step_len*l_tick)/( (100 - gait[i][1][0]) + gait[i][0][1])
					set_on_guide(i, (s_tick - step_len/2))
					
				if  tick > gait[i][0][0] and tick < gait[i][0][1]:
					l_tick = (tick+100) - gait[i][1][0]
					s_tick = (step_len*l_tick)/( (100 - gait[i][1][0]) + gait[i][0][1])
					set_on_guide(i, (s_tick - step_len/2))
				
			else:
				if local_poss[i][1] >= base_height - step_height:
					local_poss[i][1] -= speed
					
				l_tick = tick - gait[i][0][1] # Start
				s_tick = (step_len*l_tick)/(gait[i][1][0]-gait[i][0][1]) # Total Length
				set_on_guide(i, step_len - (s_tick + step_len/2))
				
		except:
			
			if tick > gait[i][0] and tick < gait[i][1]:
				if local_poss[i][1] <= base_height:
					local_poss[i][1] += speed
				l_tick = tick - gait[i][0]
				s_tick = (step_len*l_tick)/(gait[i][1]-gait[i][0])
				set_on_guide(i, s_tick - step_len/2)
				
			else:
				if local_poss[i][1] >= base_height - step_height:
					local_poss[i][1] -= speed
				l_tick = tick - gait[i][1]
				s_tick = (step_len*l_tick)/(100 - gait[i][1])
				set_on_guide(i, step_len - (s_tick + step_len/2))

def draw_gait_info(pos, size, gait, t): # [0-3]:gait
	def draw_slot(s, length):
		start = (size[0]*length[0])/100
		stop = (size[0]*length[1])/100
		middle = (start+stop) / 2
		cpos = [pos[0]-(size[0]/2)+middle,(size[1]/8)+(size[1]*s)/4]
		draw_rect(cpos, [stop-start,size[1]/4.2], r.blue, 0)
	
	for i in range(4):
		try:
			test = gait[i][0][0]
			draw_slot(i, gait[i][0])
			draw_slot(i, gait[i][1])
		except(TypeError):
			draw_slot(i, gait[i])
	
	draw_rect(pos,size, r.green, 5)
	x = (size[0]*t)/100
	pygame.draw.line(screen, r.black, [(pos[0]+x)-size[0]/2,pos[1]-size[1]/2],[(pos[0]+x)-size[0]/2,pos[1]+size[1]/2], 5)
	


spawn_leg([850,400], 1)
spawn_leg([850,200], 2)
spawn_leg([600,200], 3)
spawn_leg([600,400], 4)

axis2 = axis3 = 0
sp = 0

height = 20

curr_foot = 1
_t = 30
running = True
while running:
	clock.tick(60)
	_t += sp
	tick = (_t%100)
	screen.fill(r.white)
	
	# axis2 = joystick.get_axis(2)
	# axis3 = joystick.get_axis(3)
	
	guides[0][1] = 180 - math.degrees(math.atan2(axis2, axis3))
	guides[1][1] = 180 - math.degrees(math.atan2(axis2, axis3))
	guides[2][1] = 180 - math.degrees(math.atan2(axis2, axis3))
	guides[3][1] = 180 - math.degrees(math.atan2(axis2, axis3))


	draw_overhead_view([160,160],[320,320], curr_foot)
	draw_gait_info([480,80],[320,160], walk_gait, tick)
	move_legs(tick, 175, 20, 3, 50, walk_gait) # base_height, step_height, speed, step_len
	
	get_end_effectors()
	for item in legs:
		item.update(end_effs[item.leg_id-1][0], end_effs[item.leg_id-1][1])

	update_screen()
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			# pwm.setPWM(0,0,0)
			# pwm.setPWM(1,0,0)
			# pwm.setPWM(2,0,0)
			# pwm.setPWM(3,0,0)
			# pwm.setPWM(4,0,0)
			# pwm.setPWM(5,0,0)
			# pwm.setPWM(6,0,0)
			# pwm.setPWM(7,0,0)
			# pwm.setPWM(8,0,0)
			# pwm.setPWM(9,0,0)
			# pwm.setPWM(10,0,0)
			# pwm.setPWM(11,0,0)
			running = False
			pygame.quit()
		if i.type == KEYDOWN:
			if i.key == K_f:
				for j in range(0,4):
					guides[j][1] -= 12
			if i.key == K_g:
				for j in range(0,4):
					guides[j][1] += 12
			
			if i.key == K_q:
				helpme -= 1
				pass
			if i.key == K_w:
				helpme += 1
				pass
				
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
			
			if i.key == K_KP_PLUS:
				sp +=.2
			if i.key == K_KP_MINUS:
				sp -= .2
				
			if i.key == K_KP8:
				axis3 = sp*-1
			if i.key == K_KP2:
				axis3 = sp
			if i.key == K_KP4:
				axis2 = sp*-1
			if i.key == K_KP6:
				axis2 = sp
			if i.key == K_KP5:
				axis2 = axis3 = 0
			
			
			
