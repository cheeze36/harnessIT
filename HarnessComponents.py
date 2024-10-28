import pygame

import HarnessITUtils as utils

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, parent, pinnum, offeset):
        self.rect = pygame.rect.Rect(0,0,10,10)
        self.rect.center= pos
        self.parent = parent
        self.pinnum = pinnum
        self.offset = offeset
    def set_color(self,astr):
        self.parent.set_color(astr)
    def get_color(self):
        return self.parent.get_color()
    def set_gauge(self,astr):
        self.parent.set_gauge(astr)
    def get_gauge(self):
        return self.parent.get_gauge()
    def set_name(self,astr):
        self.parent.set_name(astr)
        print("saved "+ astr)
    def get_name(self):
        return self.parent.get_name()

class Connector(pygame.sprite.Sprite):
    def __init__(self,Image,pos, name ="??",partnumber = "",connections = 1):
        pygame.sprite.Sprite.__init__(self)
        self.imageFile = Image
        self.image = utils.loadImage(self.imageFile)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.name = name
        self.partNumber = partnumber
        self.connections = int(connections)
        self.nodes = []
        self.direction = "right"
        self.load_nodes()
    def flip(self):
        self.image = pygame.transform.flip(self.image,1,0)
        if self.direction == "left":
            self.direction = "right"
        else:
            self.direction = "left"
        print(self.direction)
    def load_nodes(self):
        print(self.direction)
        increments = self.rect.height / self.connections
        c = 0 - increments / 2
        for i in range(self.connections):
            c += increments
            self.nodes.append(Node((self.rect.right,self.rect.top + c),self,i,c))
    def update(self):
        for n in self.nodes:
            if self.direction == "right":
                n.rect.center = (self.rect.right,self.rect.top + n.offset)
            else:
                n.rect.center = (self.rect.left, self.rect.top + n.offset)
    def set_name(self,astr):
        self.name = astr
    def get_name(self):
        return self.name
class Wire():
    def __init__(self):
        self.nodeA = None
        self.nodeB = None
        self.nodeC = None
        self.nodeD = None
        self.name = "??"
        self.partnumber = ""
        self.color = "WHITE"
        self.gauge = "32"
        self.length = "0"

    def set_nodes(self,a,b,c,d):
        self.nodeA = a
        self.nodeB = b
        self.nodeC = c
        self.nodeD = d
    def set_color(self,astr):
        self.color = astr
    def get_color(self):
        return self.color
    def set_gauge(self,astr):
        self.gauge = astr
    def get_gauge(self):
        return self.gauge
    def set_name(self, astr):
        self.name = astr
        print("saved " + astr)
        print("saved " + self.name)
    def get_name(self):
        return self.name






