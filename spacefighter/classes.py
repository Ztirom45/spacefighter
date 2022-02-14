import pygame
from math import *
import function, time
from array_functions import *

class Actor: #class for player, ...
	def __init__(self,screen,img,xy=(512,350),angle=0,scale=1,health=10,maxspeed=10,speed=0):#init, paramete
		self.img_dict = function.load_img("image")
		self.img = img
			
		self.x = xy[0]
		self.y = xy[1]
		self.health = health
		self.angle = angle
		self.scale = scale
		self.screen = screen
		self.speed = speed
		self.debug = False
		self.rect = self.img_dict[self.img].get_rect()
		self.rect.x = xy[0]
		self.rect.y = xy[1]
		self.st_rect = self.rect
		
	def draw(self,xy=(0,0)):
		img2 = self.img_dict[self.img]
		img2 = pygame.transform.rotozoom(img2,-self.angle,self.scale)
		self.rect = img2.get_rect()
		rx = (img2.get_rect().w-self.st_rect.w)/2
		ry = (img2.get_rect().h-self.st_rect.h)/2
		self.rect.x = self.x-rx
		self.rect.y = self.y-ry
		#self.rect.w -= rx
		#self.rect.h -= ry
		self.screen.blit(img2,(self.x+xy[0]-rx,self.y+xy[1]-ry))
		if self.debug: pygame.draw.rect(self.screen,(255,0,0),(self.rect.x,self.rect.y,self.rect.w,self.rect.h),1)
		
		
	def move(self,steps):
	  self.x += cos(self.dirc/180*pi)*self.speed*steps
	  self.y += sin(self.dirc/180*pi)*self.speed*steps
	def change_costume(self,costume):
		self.img = costume
	
	def tudch(self,rect):
		img2 = self.img_dict[self.img]
		img2 = pygame.transform.rotozoom(img2,-self.angle,self.scale)
		self.rect = img2.get_rect()
		rx = (img2.get_rect().w-self.st_rect.w)/2
		ry = (img2.get_rect().h-self.st_rect.h)/2
		self.rect.x = self.x-rx
		self.rect.y = self.y-ry
		return pygame.Rect.colliderect(self.rect,rect)

class Actors: #class for star, astoroids, ...
	def __init__(self,screen,img,liste,player=(512,350,0),xy=0,angle=0,scale=0,health=0,maxspeed=0,speed=10,costume=0,rect=0,friction=1):#init, parameter
		
		self.img_dict = function.load_img("image") #dict
		self.img = img
		self.img_list = [img]
		self.img_bool = False
		self.xy = xy
		self.health = health
		self.angle = angle
		self.scale = scale
		self.screen = screen
		self.speed = speed
		self.friction = friction #speed lost betwin 1 and 0; 1 = no friction 0 = 100% fricton
		self.st_rect = (self.img_dict[self.img].get_rect().w,self.img_dict[self.img].get_rect().h)
		self.debug = False
		self.playerx = player[0]
		self.playery = player[1]
		self.playerpos = [player[0],player[1]]
		self.player_angle = player[2]
		self.liste = liste
		self.costume=costume
		self.sc_wh = (1024,710)
		self.rect = rect
		self.rects = []
		self.rectsave = 0
		self.std_rotozoom = [0,1]
		self.draw_exec = ""
		
	def draw(self):
		img1 = self.img_dict[self.img]
		
		if self.std_rotozoom != [0,1]:img1 = pygame.transform.rotozoom(img1,self.std_rotozoom[0],self.std_rotozoom[1])
		
		img2 = img1
		self.rects = []
		conter = 0
		#
		for i in self.liste:                        

			if all((
					i[self.xy][0]+self.playerx < self.sc_wh[0],
					i[self.xy][0]+self.playerx+self.playerpos[0] > 0,
					i[self.xy][1]+self.playery< self.sc_wh[1],
					i[self.xy][1]+self.playery+self.playerpos[1] > 0
					)):
				if(self.costume):
				  img1 = self.img_dict[self.img_list[i[self.costume]]]
				  if self.std_rotozoom != [0,1]:img1 = pygame.transform.rotozoom(img1,self.std_rotozoom[0],self.std_rotozoom[1])
				img2 = img1
				if self.scale and self.angle:            
					img2 = pygame.transform.rotozoom(img1,-i[self.angle],i[self.scale])#
				elif self.angle:
				  img2 = pygame.transform.rotozoom(img1,-i[self.angle],1)
				elif self.scale:
				  img2 = pygame.transform.rotozoom(img1,0,i[self.scale])
				if self.rectsave:
				  i[self.rect] = img2.get_rect()
				  i[self.rect].x = i[self.xy][0]+self.playerx+self.playerpos[0]
				  i[self.rect].y = i[self.xy][1]+self.playery+self.playerpos[1]
				  self.rects.append([i[self.rect],conter])
				exec(self.draw_exec)
				self.screen.blit(img2,(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1]))
				if self.debug:
				  if self.rect:pygame.draw.rect(self.screen,(255,0,0),(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1],i[self.rect][2],i[self.rect][3]),1)   
				  else:pygame.draw.rect(self.screen,(255,0,0),(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1],img2.get_rect().w,img2.get_rect().h),1)
			conter += 1      
	def move_self(self):
		z = 0
		for i in self.liste:
			i[self.xy][0] += cos(i[self.angle]/180*pi)*i[self.speed]
			i[self.xy][1] += sin(i[self.angle]/180*pi)*i[self.speed]
			
			i[self.speed] *= self.friction
			if i[self.xy][0] > 5000:#
				i[self.xy][0] = -4999
			if i[self.xy][0] < -5000:#
				 i[self.xy][0] = 4999
			if i[self.xy][1] > 5000:#
				 i[self.xy][1] = -4999
			if i[self.xy][1] < -5000:#
				 i[self.xy][1] = 4999
			if self.img == "shot":
				if i[self.speed] < 1:
					del(self.liste[z])
					break
				z += 1
						 
	def move_player_cords(self,steps):
		self.playerx += cos(self.player_angle/180*pi)*steps
		self.playery += sin(self.player_angle/180*pi)*steps
		#if "astoroid" in self.img:
		  
	def change_costume(self,costume):
		self.img = costume
	
	def tudch_pos(self,pos):
		z = 0
		img1 = self.img_dict[self.img]
		if self.std_rotozoom != [0,1]:	img1 = pygame.transform.rotozoom(img1,self.std_rotozoom[0],self.std_rotozoom[1])
		img2 = img1
		for i in self.liste:
			if(self.costume):
				img1 = self.img_dict[self.img_list[i[self.costume]]]
				if self.std_rotozoom != [0,1]:	img1 = pygame.transform.rotozoom(img1,self.std_rotozoom[0],self.std_rotozoom[1])
			img2 = img1
			if self.scale and self.angle:img2 = pygame.transform.rotozoom(img1,-i[self.angle],i[self.scale])#
			elif self.angle:img2 = pygame.transform.rotozoom(img1,-i[self.angle],1)
			elif self.scale:img2 = pygame.transform.rotozoom(img1,0,i[self.scale])
			rect1 = img2.get_rect()
			rect1.x,rect1.y = add2_pos(i[self.xy],self.playerpos) #y = rect i = list i.y = rect.y = i.x = rect.x
			rect1.x += self.playerx
			rect1.y += self.playery
			if rect1.collidepoint(pos):
				return [z]
			z+=1

class Inventory_class(Actors):
	def __init__(self,screen,img,liste,iteam_list=[],player=(512,350,0),iteam_pos=2,xy=0,scale=0,costume=0,rect=0,font_l=20,font_color=(255,255,255)):
		super().__init__(screen,
					 img,
					 liste,
					 player=player,
					 xy=xy,
					 scale=scale,
					 costume=costume,
					 rect=rect,
					 angle=0,
					 health=0,
					 maxspeed=0,
					 speed=0,
					 friction=0)
		self.iteam_images =  []
		self.iteam_pos = iteam_pos
		self.fontl = font_l
		self.font_color = font_color
		self.arial = pygame.font.SysFont('arial',font_l)
	
		for i in iteam_list:
			self.iteam_images.append(self.img_dict[i])
		inventory_script = open("Inventory_script.py","r")
		self.draw_exec = inventory_script.read()


	def change_iteam(self,pos,iteam,change_costume_bool=1):
		iteam_in = [0,0]
		if iteam[0] != self.liste[pos][2]:
			iteam_in[0] = self.liste[pos][self.iteam_pos]
			iteam_in[1] = self.liste[pos][3]
			self.liste[pos][self.iteam_pos] = iteam[0]
			self.liste[pos][3] = iteam[1]
		else:
			self.liste[pos][3] += iteam[1]
		if change_costume_bool:
			if iteam[0]:
				self.liste[pos][1] = 1
			else:
				self.liste[pos][1] = 0
		return iteam_in
  
	def half_iteam(self,pos,change_costume_bool=1):
		iteam_in = [0,0]
		#print(self.liste[pos])
		#iteam_in = [0,0]
		iteam_in[0] = self.liste[pos][self.iteam_pos]
		iteam_in[1] = self.liste[pos][3]
		self.liste[pos][3] = int(self.liste[pos][3]/2)
		iteam_in[1] /= 2
		if iteam_in[1] > int(iteam_in[1]): iteam_in[1]+= 1
		iteam_in[1] = int(iteam_in[1])
		if change_costume_bool:
			if self.liste[pos][3]:
				self.liste[pos][1] = 1
			else:
				self.liste[pos][1] = 0
				self.liste[pos][2] = 0
		return iteam_in
	
	def add_iteam(self,pos,iteam,count):
		if self.liste[pos][2] == iteam or self.liste[pos][2] == 0:
			self.liste[pos][1] = 1
			self.liste[pos][2] = iteam
			self.liste[pos][3] += count
	
class Iconbar():
	def __init__(self,screen,img,count,maxcount,rect,rot=0,scale=1,ofimg=0,bagground=0,box=0,boxsize=0):
		self.screen = screen
		self.img_dict = function.load_img("image") #dict
		self.img = img
		self.count = count
		self.maxcount = maxcount
		self.rect = rect
		self.bagground = bagground
		self.box = box
		self.boxsize = boxsize 
		self.icon_abs = rect.w/maxcount
		self.rot = rot
		self.scale = scale
		self.ofimg = ofimg
	def draw(self):
		self.icon_abs = self.rect.w/self.maxcount
		img2 = self.img_dict[self.img]
		if self.bagground:	pygame.draw.rect(self.screen,self.bagground,self.rect)
		if self.box:	pygame.draw.rect(self.screen,self.box,self.rect,self.boxsize)
		if self.rot != 0 or self.scale != 1:	img2 = pygame.transform.rotozoom(self.img_dict[self.img],self.rot,self.scale)
		if self.ofimg:	img3 = pygame.transform.rotozoom(self.img_dict[self.ofimg],self.rot,self.scale)
		for i in range(self.maxcount):
			if i < self.count:	self.screen.blit(img2,(i*self.icon_abs+self.rect.x,self.rect.y))
			elif self.ofimg:	self.screen.blit(img3,(i*self.icon_abs+self.rect.x,self.rect.y))
			else:
				for i in range(self.maxcount):
					if i < self.count:	self.screen.blit(self.img_dict[self.img],(i*self.icon_abs+self.rect.x,self.rect.y))
					elif self.ofimg:	self.screen.blit(self.img_dict[self.ofimg],(i*self.icon_abs+self.rect.x,self.rect.y))


class Timer:
	def __init__(self):
		self._start_time = 0

	def start(self):
		self._start_time = time.perf_counter()
		
	def get_time(self):
		return time.perf_counter() - self._start_time



