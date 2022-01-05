import pygame
from math import *
import function

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
    def __init__(self,screen,img,liste,player=(512,350,0),xy=0,angle=0,scale=0,health=0,maxspeed=0,speed=0,costume=0,friction=1):#init, parameter
        
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
        self.playerpos = (512,350)
        self.player_angle = player[2]
        self.liste = liste
        self.costume=costume
        self.sc_wh = (1024,710)
        self.rect = 0
        self.rects = []
        self.rectsave = 0
        
    def draw(self):
        img1 = self.img_dict[self.img]
        img2 = img1
        self.rects = []
        #print(self.rects)
        conter = 0
        for i in self.liste:                        
            

            if all((
                    i[self.xy][0]+self.playerx < self.sc_wh[0],
                    i[self.xy][0]+self.playerx+self.playerpos[0] > 0,
                    i[self.xy][1]+self.playery< self.sc_wh[1],
                    i[self.xy][1]+self.playery+self.playerpos[1] > 0
                    )):
                if self.img_bool:
                    img1 = self.img_dict[self.img_list[i[self.img_bool]]]
                if self.scale and self.angle:            
                    img2 = pygame.transform.rotozoom(img1,-i[self.angle],i[self.scale])#
                elif self.angle:
                  img2 = pygame.transform.rotozoom(img1,-i[self.angle],1)
                elif self.scale:
                  img2 = pygame.transform.rotozoom(img1,0,i[self.scale])
                if self.rectsave:
                  rectsave = img2.get_rect()
                  rectsave.x = i[self.xy][0]+self.playerx+self.playerpos[0]
                  rectsave.y = i[self.xy][1]+self.playery+self.playerpos[1]
                  self.rects.append([rectsave,conter])
                  
                self.screen.blit(img2,(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1]))
                if self.debug:
                  if self.rect:pygame.draw.rect(self.screen,(255,0,0),(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1],i[self.rect][2],i[self.rect][3]),1)   
                  else:pygame.draw.rect(self.screen,(255,0,0),(i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1],img2.get_rect().w,img2.get_rect().h),1)
                if img2.get_rect().collidepoint(self.playerx+self.playerpos[0],self.playery+self.playerpos[1]):
                    print("hi")
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
              z += 1
                         
    def move_player_cords(self,steps):
        self.playerx += cos(self.player_angle/180*pi)*steps
        self.playery += sin(self.player_angle/180*pi)*steps
        #if "astoroid" in self.img:
          
    def change_costume(self,costume):
        self.img = costume
