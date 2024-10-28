import pygame
from enum import Enum,auto


COLORS = {"RED":(255,0,0),"WHITE":(255,255,255),"BLUE":(0,0,255),"GREEN":(0,255,0)}
GAUGE = {"32":1,"30":1,"28":2,"26":2,"24":3,"22":3,"20":3,
         "18":4,"16":4,"14":5,"12":6,"10":7,"8":8,
         "6":9,"4":10,"2":11,"1":12,"1/0":13,"2/0":14,"3/0":15,"4/0":16}


def loadImage(filename, alpha=0):
    try:
        imgdir = filename
        print(imgdir)
        image = pygame.image.load(imgdir)
        if image == None:
            image = pygame.Surface(64,64)
            image.fill((255,0,0))
        if alpha == 1:
            image.set_colorkey(image.get_at((0,0)))
            image.convert_alpha()
        else:
            image.convert()
            #image.set_colorkey(image.get_at((0,0)))
        return image
    except:
        print("couldn't load image " + filename)

def outline_image(image, surface,pos,size = 1,color = (255,255,255)):
    mask = pygame.mask.from_surface(image)
    outline = mask.to_surface(setcolor=color)
    outline.set_colorkey((0,0,0))
    surface.blit(outline,add_pos(pos,(size,0)))
    surface.blit(outline, add_pos(pos, (-size, 0)))
    surface.blit(outline, add_pos(pos, (0,size)))
    surface.blit(outline, add_pos(pos, (0,-size)))

def add_pos(pos1, pos2):
    x = pos1[0] + pos2[0]
    y = pos1[1] + pos2[1]
    return (x, y)
def divide_pos(pos1, pos2):
    x = pos1[0] / pos2[0]
    y = pos1[1] / pos2[1]
    return (x, y)
def multiply_pos(pos1, pos2):
    x = pos1[0] * pos2[0]
    y = pos1[1] * pos2[1]
    return (x, y)
def setx(pos,num):
    x = num
    y = pos[1]
    return (x,y)
def sety(pos,num):
    x = pos[0]
    y = num
    return (x,y)