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
    a = [[[randint(-5000,5000),randint(-5000,5000)]] for x in range(5000)]
    b = [[[randint(-5000,5000),
            randint(-5000,5000)],
           randint(0,360),
           randint(0,11),
           randint(5,15)/10,
           randint(0,2)] for x in range(500)]
    img_dict = load_img("image")
    img_list = [
        "astoroid1",
        "astoroid2",
        "astoroid3",]
    for x in b:
              c = img_dict[img_list[x[4]]]
              c = pygame.transform.rotozoom(c,-x[1],x[3])
              x.append(tuple(c.get_rect()))
              
    dump([a,b],f)
    f.close() #write random stars in file

def load_space(file): #load all stars
    f = open(file+".dat","rb") #open file
    l = load(f) # load file in list l
    f.close() #close file
    return l # gives list l return
