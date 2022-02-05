print("control: w a s d \nshot: space\nDebug:F1")

import pygame, random, time
import function
from classes import *
from array_functions import *   
pygame.init()

function.reset_space("space")
function.reset_player("player")
stars,astoroids,spaceships = function.load_file("space")

player_cords,iteam_list,inventory_list = function.load_file("player")

global_img_dict = function.load_img("image")

font_l = 20
arial = pygame.font.SysFont('arial', font_l)

screen = pygame.display.set_mode()
sc_size = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2,0]
clock = pygame.time.Clock()

player = Actor(screen,'prismfighter',xy=(sc_size[0],sc_size[1]),speed=10,health=10)


star = Actors(screen,"star",stars,player=sc_size)
star.sc_wh = pygame.display.get_window_size()


astoroid = Actors(screen,"astoroid1",astoroids,player=sc_size,angle=1,speed=2,scale=3,costume=4)
astoroid.img_list.append("astoroid2")
astoroid.img_list.append("astoroid3")
astoroid.img_bool=4
astoroid.rect = 5
astoroid.rectsave = 1
astoroid.sc_wh = pygame.display.get_window_size()

astoroid_explosion = Actors(screen,"astoroid_explosion1",[],player=sc_size,angle=1,speed=2,scale=3,costume=4)
astoroid_explosion.img_list.append("astoroid_explosion2")
astoroid_explosion.img_list.append("astoroid_explosion3")
astoroid_explosion.sc_wh = pygame.display.get_window_size()

opponent = Actors(screen,"spaceship1",spaceships,player=sc_size,angle=1,speed=2,scale=3,costume=4)
opponent.img_list.append("spaceship2")
opponent.sc_wh = pygame.display.get_window_size()

lives = Iconbar(screen,"health2",10,10,pygame.Rect(sc_size[0]-200,10,100,20),ofimg="health")
lives.count = player.health

Inventory_Frames = Actors(screen,"Inventory_Frame",inventory_list,player=(10,10,0),costume=2)
Inventory_Frames.img_list.append("Inventory_Frame2")
Inventory_Frames.img_list.append("Inventory_Frame3")
Inventory_Frames.img_list.append("Inventory_Frame4")
Inventory_Frames.img_list.append("Inventory_Frame_Plus")
Inventory_Frames.sc_wh = pygame.display.get_window_size()
Inventory_Frames.std_rotozoom = [0,3]

fps = 60 # max 120
shot = Actors(screen,"shot",[],player=sc_size,angle=1,speed=2,rect=3,friction=0.97)
shot.fricton = 0.999999999999999
shot.rectsave = 1
shot.sc_wh = pygame.display.get_window_size()
shot_cooldown = 0.1
shot_timer = Timer()

shot_sound = pygame.mixer.Sound('sounds\laser.wav')
astoroid_collide_player = pygame.mixer.Sound('sounds\explosion.wav')
astoroid_collide_shot = pygame.mixer.Sound('sounds\explosion.wav')

OpenInventory = 0

def tudch_astoroid():
    global astoroid
    global player
    for x in astoroid.rects:
        superbreak = 0
        if player.tudch(x[0]):
            astoroid_explosion.liste.append(astoroid.liste[x[1]]+[0])
            del(astoroid.liste[x[1]])
            player.health -= 1
            pygame.mixer.Channel(2).play(astoroid_collide_player)   
            superbreak = 1
            break
        if not(superbreak):
            for y in shot.rects:
                if pygame.Rect.colliderect(x[0],y[0]):
                    astoroid_explosion.liste.append(astoroid.liste[x[1]]+[0])
                    del(astoroid.liste[x[1]])
                    del(shot.liste[y[1]])
                    pygame.mixer.Channel(3).play(astoroid_collide_shot)
                    superbreak = 1
                    break
        
        if superbreak:break
    counter = 0
    
    for x in astoroid_explosion.liste:
        if x[6] > 10:#            pos   angle speed size costume
            if x[3]>0.5:
                astoroid.liste.append([x[0],x[1]+45,x[2]/2,x[3]/2,x[4],x[5]])
                #astoroid.liste.append([x[0],x[1]-45,x[2]/2,x[3]/2,x[4],x[5]])
            del(astoroid_explosion.liste[counter])
            break
        else:
            astoroid_explosion.liste[counter][6] += 1
            
def border():
    if star.playerx > 5000:#
     star.playerx = -4999
     astoroid.playerx = -4999
     astoroid_explosion.playerx = -4999
     shot.playerx = -4999
    if star.playerx < -5000:#
     star.playerx = 5000
     astoroid.playerx = 5000
     astoroid_explosion.playerx = 5000
     shot.playerx = 5000
     
    if star.playery > 5000:#
     star.playery = -4999
     astoroid.playery = -4999
     astoroid_explosion.playery = -4999
     shot.playery = -4999
    if star.playery < -5000:#
     star.playery = 4999
     astoroid.playery = 4999
     astoroid_explosion.playery = 4999
     shot.playery = 4999
     
def player_shot():
    global player
    global shot
    pygame.mixer.Channel(0).play(shot_sound)
    shot.liste.append([[-(shot.playerx),-(shot.playery)],player.angle,30,pygame.Rect(0,0,0,0)])
    
def screen_update():
    fps_now = clock.get_fps()
    global screen
    global fps
    screen.fill((0,0,0))

    star.draw()
    astoroid.move_self()
    astoroid.draw()
    astoroid_explosion.move_self()
    astoroid_explosion.draw()
    shot.move_self()
    shot.draw()
    opponent.move_self()
    opponent.draw()
    player.draw()
    lives.draw()

    
    if player.debug == True:
        screen.blit(arial.render(str(int(star.playerx))+"/"+str(int(star.playery)), True, (255,0,0)),(0,0))
        screen.blit(arial.render("fps: "+str(fps_now)+" / "+str(fps), True, (255,0,0)),(0,font_l))
    
    pygame.display.update()
def update():
    global go
    tudch_astoroid()
    lives.count = player.health
    if player.health <=0:
        gameover()
        go = False
    
def player_contr():
    global player
    global astoroid
    global star
    global events
    global shot
    global OpenInventory
    pres = pygame.key.get_pressed() 
    if pres[pygame.K_w]:
        star.move_player_cords(-2*player.speed)
        astoroid.move_player_cords(-2*player.speed)
        astoroid_explosion.move_player_cords(-2*player.speed)
        shot.move_player_cords(-2*player.speed)
        opponent.move_player_cords(-2*player.speed)
        
    if pres[pygame.K_s]:
        star.move_player_cords(player.speed)
        astoroid.move_player_cords(player.speed)
        astoroid_explosion.move_player_cords(player.speed)
        shot.move_player_cords(player.speed)
        opponent.move_player_cords(player.speed)
        
    if pres[pygame.K_d]:
     player.angle += player.speed
     star.player_angle += player.speed
     astoroid.player_angle += player.speed
     astoroid_explosion.player_angle += player.speed
     shot.player_angle += player.speed
     opponent.player_angle += player.speed
    if pres[pygame.K_a]:
     player.angle -= player.speed
     astoroid.player_angle -= player.speed
     astoroid_explosion.player_angle -= player.speed
     star.player_angle -= player.speed
     shot.player_angle -= player.speed
     opponent.player_angle -= player.speed
    if pres[pygame.K_SPACE] and shot_timer.get_time() > shot_cooldown:
        shot_timer.start()
        player_shot()
        

    
    border()
    for l_event in events:
        if l_event.type == pygame.KEYDOWN:
            if l_event.key == pygame.K_F1:
                if player.debug:
                    player.debug = False
                    star.debug = False
                    astoroid.debug = False
                    astoroid_explosion.debug = False
                    shot.debug = False
                else:
                    player.debug = True
                    star.debug = True
                    astoroid.debug = True
                    astoroid_explosion.debug = True
                    shot.debug = True
            if l_event.key == pygame.K_e:
                if OpenInventory == False:
                   OpenInventory = True

def Inventory():
    global events
    global OpenInventory
    img1 = pygame.transform.rotozoom(global_img_dict["prismfighter"],90,5)
    screen.fill((0,0,0))
    spaceship_point = sub2_pos(div_pos(star.sc_wh,2),div_pos([img1.get_rect().w,img1.get_rect().h],2))
    spaceship_name = arial.render("prismfighter", True, (255,255,255))
    screen.blit(spaceship_name,(star.sc_wh[0]/2-spaceship_name.get_rect().w/2,spaceship_point[1]-font_l))
    screen.blit(img1,spaceship_point)
    
    for l_event in events:
        if l_event.type == pygame.KEYDOWN:
            if l_event.key == pygame.K_e:
                if OpenInventory == True:
                    OpenInventory = False
        if l_event.type == pygame.MOUSEBUTTONUP:
            if Inventory_Frames.tudch_pos(pygame.mouse.get_pos()):
                tudch_fellt = Inventory_Frames.tudch_pos(pygame.mouse.get_pos())
                # print(tusch_fellt)
                Inventory_Frames.liste[tudch_fellt[0]][Inventory_Frames.costume] += 1
                if Inventory_Frames.liste[tudch_fellt[0]][Inventory_Frames.costume] > len(Inventory_Frames.img_list)-1:
                    Inventory_Frames.liste[tudch_fellt[0]][Inventory_Frames.costume] = 0
    Inventory_Frames.draw()
    pygame.display.update()
    
    

def gameover():
    lives.draw
    gameoverfont = pygame.font.SysFont('arial', 100)
    screen.blit(gameoverfont.render("Game Over", True, (255,0,0)),(300,300))
    pygame.display.update()
    #time.sleep(3)



go = True  
shot_timer.start()
pygame.mixer.music.load("sounds/laser.wav")


while go:
    events = pygame.event.get()
    for l_event in events:
        if l_event.type == pygame.QUIT:
            go = False
    if OpenInventory == False:
        screen_update()
        player_contr()
        update()
    else:
        Inventory()
    clock.tick(fps)
    

pygame.quit()
