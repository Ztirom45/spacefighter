import os,pygame,math #import all
from pickle import *
from random import *
from PIL import Image
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


def get_true(image_path): #get a image with cords for every color and nothing for every trasparent
	img = Image.open(image_path)
	a = list(img.getdata())
	liste = []
	for i in range(img.size[0]):    # For every pixel:
		for j in range(img.size[1]):
			f = a[j*img.size[0]+i]
			if  f != (0,0,0,0):
				liste.append([i,j])

	return liste
def set_pos(true_img,xy):#move a trueimage to a cord
	a = [[x[0]+xy[0],x[1]+xy[1]] for x in true_img]
	return a
	
def tudch(true_img1,true_img2):#true image tudch an other
	for x in true_img1:
		for y in true_img2:
			if y == x:
				return True
	return False
	
"""
def get_true_combi(image,path="image",angle=0,zoom=1,xy=(0,0)):
    img = pygame.image.load(path+"/"+image+".png")
    img = pygame.transform.rotozoom(img,angle,zoom)
    img.scroll(dx=xy[0], dy=xy[1])
    #print(img)
    pygame.image.save(img,path+"/"+image+"combi.png")
    #img = 
    return get_true(path+"/"+image+"combi.png")
    #return set_pos(img,xy)
"""
#for x in range(100):
#    a = get_true_combi("astoroid1",angle=33,zoom=10,xy=(200,200))
#    print(x)
