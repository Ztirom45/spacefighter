import os,pygame,math #import all
from pickle import *
from random import *
pygame.init() #init pygame

def load_img(dir_path): #load all image 
    img = {} #image dictonerry
    try:
      for entry in os.listdir(dir_path): #list all thinggs in the folder 
        if os.path.isfile(dir_path+"/"+entry) and entry.endswith(".png"): #check png
            img[entry[:-4]] = pygame.image.load(dir_path+"/"+entry) #append image + imagename in the 
    except:
        print("error") #error
    return img #givs the image
def reset_space(file): #create random stars
    f = open(file+".dat","bw") #open file
    a = [[[randint(-6000,6000),randint(-6000,6000)]] for x in range(5000)]
    b = [[[randint(-5000,5000),
            randint(-5000,5000)],
           randint(0,360),
           randint(0,11),
           randint(5,15)/10,
           randint(0,2)] for x in range(500)]

    d = [[[randint(-5000,5000), #spaceships
            randint(-5000,5000)],
           randint(0,360),
           randint(0,11),
           3,
           randint(0,1)] for x in range(50)]
    img_dict = load_img("image")
    img_list = [
        "astoroid1",
        "astoroid2",
        "astoroid3",]
    for x in b:
              c = img_dict[img_list[x[4]]]
              c = pygame.transform.rotozoom(c,-x[1],x[3])
              x.append(tuple(c.get_rect()))
              
    dump([a,b,d],f)
    f.close() #write random stars in file
    

def reset_player(file): #create random stars
    f = open(file+".dat","bw") #open file
    fellts = 104
    dist=22*3
    a = int(fellts/10)
    b = [ [[x*dist,y*dist],0,1] for y in range(10) for x in range(a)]
    for y in range(fellts-a*10):b.append([[y*dist,a*dist],0,1])
    b[len(b)-1][2] = 4
    dump([[0,0,90,10],["void"],b],f)#player pos, angele iteam list, inventory
    f.close() #write random stars in file

def load_file(file): #load all stars
    f = open(file+".dat","rb") #open file
    l = load(f) # load file in list l
    f.close() #close file
    return l # gives list l return

#reset_space("space")
