#if compile error look at global
import pygame, random
import function
from classes import *
pygame.init()

font_l = 20
arial = pygame.font.SysFont('arial', font_l)
screen = pygame.display.set_mode((1024,710))
clock = pygame.time.Clock()
player = Actor(screen,'prismfighter')
stars,astoroids = function.load_space("space")
star = Actors(screen,"star",stars)
astoroid = Actors(screen,"astoroid1",astoroids,angle=1,speed=2,scale=3,costume=4)
astoroid.img_list.append("astoroid2")
astoroid.img_list.append("astoroid3")
astoroid.img_bool=4
astoroid.rect = 5
fps = 60
player.speed = 10 #speed of player

shot = Actors(screen,"shot",[],angle=1,speed=2)

def border():
    if star.playerx > 5000:#
     star.playerx = -4999
     astoroid.playerx = -4999
     shot.playerx = -4999
    if star.playerx < -5000:#
     star.playerx = 5000
     astoroid.playerx = 5000
     shot.playerx = 5000
     
    if star.playery > 5000:#
     star.playery = -4999
     astoroid.playery = -4999
     shot.playery = -4999
    if star.playery < -5000:#
     star.playery = 4999
     astoroid.playery = 4999
     shot.playery = 4999
     
def player_shot():
    global player
    global shot
    shot.liste.append([[-(0+shot.playerx),-(0+shot.playery)],player.angle,30])
    print(-(0+shot.playerx),-(0+shot.playery))
    
def screen_update(fps):
    global screen
    screen.fill((0,0,0))


    star.draw()
    astoroid.move_self()
    astoroid.draw()
    shot.move_self()
    shot.draw()
    player_contr(fps)
    player.draw()
    
    pygame.display.update()
    

def player_contr(fps):
    global player
    global astoroid
    global star
    global events
    global shot
    pres = pygame.key.get_pressed() 
    fps_now = clock.get_fps()
    
    if pres[pygame.K_w]:
        star.move_player_cords(-2*player.speed)
        astoroid.move_player_cords(-2*player.speed)
        shot.move_player_cords(-2*player.speed)
        
    if pres[pygame.K_s]:
     star.move_player_cords(player.speed)
     astoroid.move_player_cords(player.speed)
     shot.move_player_cords(player.speed)
    if pres[pygame.K_d]:
     player.angle += player.speed
     star.player_angle += player.speed
     astoroid.player_angle += player.speed
     shot.player_angle += player.speed
    if pres[pygame.K_a]:
     player.angle -= player.speed
     astoroid.player_angle -= player.speed
     star.player_angle -= player.speed
     shot.player_angle -= player.speed
    if pres[pygame.K_SPACE]:
        player_shot()
    border()
    for l_event in events:
        if l_event.type == pygame.KEYDOWN:
            if l_event.key == pygame.K_F5:
                if player.debug:
                    player.debug = False
                    star.debug = False
                    astoroid.debug = False
                    shot.debug = False
                else:
                    player.debug = True
                    star.debug = True
                    astoroid.debug = True
                    shot.debug = True
                    
    if player.debug == True:        
        screen.blit(arial.render(str(int(star.playerx))+"/"+str(int(star.playery)), True, (255,0,0)),(0,0))
        screen.blit(arial.render("fps: "+str(fps_now)+" / "+str(fps), True, (255,0,0)),(0,font_l))
    
go = True

while go:
    events = pygame.event.get()
    for l_event in events:
        if l_event.type == pygame.QUIT:
            go = False
    print(shot.playery)
    screen_update(fps)
    clock.tick(fps)
    
pygame.quit()
