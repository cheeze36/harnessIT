"""
This module defines the drawing frame for the HarnessIT application.
"""

import tkinter

import pygame
import tkinter as tk
import os

import HarnessComponents
import HarnessITUtils

class DrawFrame():
    """
    The drawing frame for the HarnessIT application.
    """
    def __init__(self,parent,app ):#= tk.Tk()):
        """
        Initializes the DrawFrame.

        Args:
            parent: The parent widget.
            app: The main application instance.
        """
        self.app = app
        self.parent = parent
        self.frame = tk.Frame(self.parent, width =self.parent.winfo_width() - 100, height = self.parent.winfo_height() - 120)

        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.screen = pygame.display.set_mode()

        pygame.display.init()

        self.selected = []

        self.connectors = []
        self.wires =[]

    def draw(self):
        """
        Draws the harness components on the screen.
        """
        self.screen.fill(pygame.Color(100, 100, 100))
        for i in range(self.frame.winfo_width()):
            pygame.draw.line(self.screen,(155,155,155),(i * 25,0),(i * 25,self.screen.get_height()),1)
        for i in range(self.frame.winfo_height()):
            pygame.draw.line(self.screen,(155,155,155),(0,i * 25),(self.screen.get_width(),i * 25),1)
        for s in self.selected:
            if isinstance(s,HarnessComponents.Connector):
                HarnessITUtils.outline_image(s.image,self.screen,s.rect.topleft)
            elif isinstance(s,HarnessComponents.Node):
                pygame.draw.circle(self.screen, (0, 0, 0), (s.rect.center), 7)
                pygame.draw.circle(self.screen, (200, 200, 200), (s.rect.center), 5)
        for c in self.connectors:
            self.screen.blit(c.image,c.rect)
            if self.app.state == "wire":
                for n in c.nodes:
                    if n in self.app.wirenodes:
                        pygame.draw.circle(self.screen, (255, 255, 255), (n.rect.center), 7)
                        pygame.draw.circle(self.screen, (100, 155, 55), (n.rect.center), 5)
                    else:
                        pygame.draw.circle(self.screen, (255, 255, 255), (n.rect.center), 7)
                        pygame.draw.circle(self.screen,(0,155,255),(n.rect.center),5)
        for w in self.wires:
            color = HarnessITUtils.COLORS[w.get_color()]
            gauge = HarnessITUtils.GAUGE[w.get_gauge()]
            pygame.draw.line(self.screen,color,w.nodeA.rect.center,w.nodeB.rect.center,gauge)
            pygame.draw.line(self.screen, color, w.nodeB.rect.center, w.nodeC.rect.center, gauge)
            pygame.draw.line(self.screen, color, w.nodeC.rect.center, w.nodeD.rect.center, gauge)
            if self.app.state == "wire" or self.app.state == "selecting":
                pygame.draw.circle(self.screen, (200, 200, 200), (w.nodeB.rect.center), 5)
                pygame.draw.circle(self.screen, (200, 200, 200), (w.nodeC.rect.center), 5)


    def update(self):
        """
        Updates the display and the harness components.
        """
        pygame.display.update()
        for c in self.connectors:
            c.update()
    def resize(self):
        """
        Resizes the drawing frame.
        """
        self.frame.config(width =self.parent.winfo_width() - 25, height = self.parent.winfo_height() - 25)
