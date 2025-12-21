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
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)


        self.selected = []

        self.connectors = []
        self.wires =[]

        self.zoom_level = 1.0
        self.view_offset = [0, 0]

    def world_to_screen(self, x, y):
        """Converts world coordinates to screen coordinates."""
        screen_x = (x - self.view_offset[0]) * self.zoom_level
        screen_y = (y - self.view_offset[1]) * self.zoom_level
        return int(screen_x), int(screen_y)

    def screen_to_world(self, x, y):
        """Converts screen coordinates to world coordinates."""
        world_x = x / self.zoom_level + self.view_offset[0]
        world_y = y / self.zoom_level + self.view_offset[1]
        return int(world_x), int(world_y)

    def snap_to_grid(self, x, y):
        """Snaps the given coordinates to the nearest grid intersection."""
        grid_size = self.app.grid_size
        snapped_x = round(x / grid_size) * grid_size
        snapped_y = round(y / grid_size) * grid_size
        return snapped_x, snapped_y

    def zoom(self, event):
        """Zooms the view in or out."""
        mouse_pos_before_zoom = self.screen_to_world(event.x, event.y)

        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
        
        self.zoom_level = max(0.1, min(self.zoom_level, 5.0))

        mouse_pos_after_zoom = self.screen_to_world(event.x, event.y)

        self.view_offset[0] += mouse_pos_before_zoom[0] - mouse_pos_after_zoom[0]
        self.view_offset[1] += mouse_pos_before_zoom[1] - mouse_pos_after_zoom[1]


    def draw(self):
        """
        Draws the harness components on the screen.
        """
        self.screen.fill(pygame.Color(100, 100, 100))
        
        # Draw grid
        if self.app.grid_visible.get():
            grid_size = self.app.grid_size
            
            start_x, start_y = self.screen_to_world(0, 0)
            end_x, end_y = self.screen_to_world(self.screen.get_width(), self.screen.get_height())

            for x in range(start_x - (start_x % grid_size), end_x, grid_size):
                start_pos = self.world_to_screen(x, start_y)
                end_pos = self.world_to_screen(x, end_y)
                pygame.draw.line(self.screen, (155, 155, 155), start_pos, end_pos, 1)

            for y in range(start_y - (start_y % grid_size), end_y, grid_size):
                start_pos = self.world_to_screen(start_x, y)
                end_pos = self.world_to_screen(end_x, y)
                pygame.draw.line(self.screen, (155, 155, 155), start_pos, end_pos, 1)


        for s in self.selected:
            if isinstance(s,HarnessComponents.Connector):
                screen_pos = self.world_to_screen(s.rect.x, s.rect.y)
                scaled_image = pygame.transform.scale(s.image, (int(s.rect.width * self.zoom_level), int(s.rect.height * self.zoom_level)))
                HarnessITUtils.outline_image(scaled_image,self.screen,screen_pos)
            elif isinstance(s,HarnessComponents.Node):
                screen_pos = self.world_to_screen(s.rect.centerx, s.rect.centery)
                pygame.draw.circle(self.screen, (0, 0, 0), screen_pos, 7)
                pygame.draw.circle(self.screen, (200, 200, 200), screen_pos, 5)

        for c in self.connectors:
            screen_pos = self.world_to_screen(c.rect.x, c.rect.y)
            scaled_image = pygame.transform.scale(c.image, (int(c.rect.width * self.zoom_level), int(c.rect.height * self.zoom_level)))
            self.screen.blit(scaled_image, screen_pos)

            if self.app.view_connector_names.get():
                text = self.font.render(c.name, True, (0, 0, 0))
                text_rect = text.get_rect(center=self.world_to_screen(c.rect.centerx, c.rect.centery - 20))
                self.screen.blit(text, text_rect)

            if self.app.state == "wire":
                for n in c.nodes:
                    screen_pos = self.world_to_screen(n.rect.centerx, n.rect.centery)
                    if n in self.app.wirenodes:
                        pygame.draw.circle(self.screen, (255, 255, 255), screen_pos, 7)
                        pygame.draw.circle(self.screen, (100, 155, 55), screen_pos, 5)
                    else:
                        pygame.draw.circle(self.screen, (255, 255, 255), screen_pos, 7)
                        pygame.draw.circle(self.screen,(0,155,255), screen_pos,5)

            if self.app.view_pin_numbers.get():
                for n in c.nodes:
                    screen_pos = self.world_to_screen(n.rect.centerx, n.rect.centery)
                    pin_text = self.font.render(str(n.get_display_pin()), True, (0, 0, 0))
                    text_rect = pin_text.get_rect(center=screen_pos)
                    self.screen.blit(pin_text, text_rect)

        for w in self.wires:
            color = HarnessITUtils.COLORS[w.get_color()]
            gauge = HarnessITUtils.GAUGE[w.get_gauge()]
            
            for i in range(len(w.nodes) - 1):
                start_pos = self.world_to_screen(w.nodes[i].rect.centerx, w.nodes[i].rect.centery)
                end_pos = self.world_to_screen(w.nodes[i+1].rect.centerx, w.nodes[i+1].rect.centery)
                pygame.draw.line(self.screen, color, start_pos, end_pos, gauge)
            
            if self.app.view_wire_names.get():
                midpoint_x = (w.nodes[0].rect.centerx + w.nodes[-1].rect.centerx) / 2
                midpoint_y = (w.nodes[0].rect.centery + w.nodes[-1].rect.centery) / 2
                screen_pos = self.world_to_screen(midpoint_x, midpoint_y)
                text = self.font.render(w.name, True, (0, 0, 0))
                text_rect = text.get_rect(center=screen_pos)
                self.screen.blit(text, text_rect)

            if self.app.state == "wire" or self.app.state == "selecting":
                for node in w.nodes:
                    if not isinstance(node.parent, HarnessComponents.Connector):
                        screen_pos = self.world_to_screen(node.rect.centerx, node.rect.centery)
                        pygame.draw.circle(self.screen, (200, 200, 200), screen_pos, 5)


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
