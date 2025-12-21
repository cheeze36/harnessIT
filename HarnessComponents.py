"""
This module defines the core components of a harness, including nodes, connectors, and wires.
"""

import pygame
import HarnessITUtils as utils

class Node(pygame.sprite.Sprite):
    """
    A node represents a connection point on a connector or a point on a wire.
    """
    def __init__(self, pos, parent, pinnum, offset):
        """
        Initializes a Node.

        Args:
            pos (tuple): The position of the node.
            parent (Connector or Wire): The parent object of the node.
            pinnum (int): The pin number of the node.
            offset (int): The offset of the node from the parent's position.
        """
        self.rect = pygame.rect.Rect(0, 0, 10, 10)
        self.rect.center = pos
        self.parent = parent
        self.pinnum = pinnum
        self.offset = offset

    def get_display_pin(self):
        """
        Gets the display pin number, accounting for flipped connectors.
        """
        if isinstance(self.parent, Connector) and self.parent.direction == "left":
            return self.parent.connections - self.pinnum
        return self.pinnum + 1

    def set_color(self, astr):
        """
        Sets the color of the parent wire.
        """
        self.parent.set_color(astr)

    def get_color(self):
        """
        Gets the color of the parent wire.
        """
        return self.parent.get_color()

    def set_gauge(self, astr):
        """
        Sets the gauge of the parent wire.
        """
        self.parent.set_gauge(astr)

    def get_gauge(self):
        """
        Gets the gauge of the parent wire.
        """
        return self.parent.get_gauge()

    def set_name(self, astr):
        """
        Sets the name of the parent object.
        """
        self.parent.set_name(astr)

    def get_name(self):
        """
        Gets the name of the parent object.
        """
        return self.parent.get_name()

    def to_dict(self):
        """
        Returns a dictionary representation of the node.
        """
        return {
            "pos": self.rect.center,
            "pinnum": self.pinnum,
            "offset": self.offset,
        }

    @classmethod
    def from_dict(cls, data, parent):
        """
        Creates a Node from a dictionary representation.
        """
        return cls(
            pos=data["pos"],
            parent=parent,
            pinnum=data["pinnum"],
            offset=data["offset"],
        )


class Connector(pygame.sprite.Sprite):
    """
    A connector represents a physical connector in the harness.
    """
    def __init__(self, Image, pos, name="??", partnumber="", connections=1, direction="right"):
        """
        Initializes a Connector.

        Args:
            Image (str): The path to the image file for the connector.
            pos (tuple): The position of the connector.
            name (str, optional): The name of the connector. Defaults to "??".
            partnumber (str, optional): The part number of the connector. Defaults to "".
            connections (int, optional): The number of connections on the connector. Defaults to 1.
            direction (str, optional): The direction the connector is facing. Defaults to "right".
        """
        pygame.sprite.Sprite.__init__(self)
        self.imageFile = Image
        self.image = utils.loadImage(self.imageFile)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.name = name
        self.partNumber = partnumber
        self.connections = int(connections)
        self.nodes = []
        self.direction = direction
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.load_nodes()

    def flip(self, app):
        """
        Flips the connector horizontally and updates wire connections.
        """
        self.image = pygame.transform.flip(self.image, 1, 0)
        if self.direction == "left":
            self.direction = "right"
        else:
            self.direction = "left"
        
        old_nodes = self.nodes[:]
        self.load_nodes()

        for wire in app.HDF.wires:
            for i, node in enumerate(wire.nodes):
                if node in old_nodes:
                    pin_index = old_nodes.index(node)
                    new_pin_index = self.connections - 1 - pin_index
                    wire.nodes[i] = self.nodes[new_pin_index]


    def load_nodes(self):
        """
        Creates the connection nodes for the connector.
        """
        self.nodes.clear()
        increments = self.rect.height / self.connections
        c = 0 - increments / 2
        for i in range(self.connections):
            c += increments
            if self.direction == "right":
                self.nodes.append(Node((self.rect.right, self.rect.top + c), self, i, c))
            else:
                self.nodes.append(Node((self.rect.left, self.rect.top + c), self, i, c))

    def update(self):
        """
        Updates the position of the connector's nodes.
        """
        for n in self.nodes:
            if self.direction == "right":
                n.rect.center = (self.rect.right, self.rect.top + n.offset)
            else:
                n.rect.center = (self.rect.left, self.rect.top + n.offset)

    def set_name(self, astr):
        """
        Sets the name of the connector.
        """
        self.name = astr

    def get_name(self):
        """
        Gets the name of the connector.
        """
        return self.name

    def to_dict(self):
        """
        Returns a dictionary representation of the connector.
        """
        return {
            "image": self.imageFile,
            "pos": self.rect.center,
            "name": self.name,
            "partnumber": self.partNumber,
            "connections": self.connections,
            "direction": self.direction,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Connector from a dictionary representation.
        """
        return cls(
            Image=data["image"],
            pos=data["pos"],
            name=data["name"],
            partnumber=data["partnumber"],
            connections=data["connections"],
            direction=data["direction"],
        )


class Wire():
    """
    A wire represents a connection between two or more nodes.
    """
    def __init__(self, name="??", partnumber="", color="WHITE", gauge="32"):
        """
        Initializes a Wire.

        Args:
            name (str, optional): The name of the wire. Defaults to "??".
            partnumber (str, optional): The part number of the wire. Defaults to "".
            color (str, optional): The color of the wire. Defaults to "WHITE".
            gauge (str, optional): The gauge of the wire. Defaults to "32".
        """
        self.nodes = []
        self.lengths = []
        self.name = name
        self.partnumber = partnumber
        self.color = color
        self.gauge = gauge

    def add_node(self, node):
        """
        Adds a node to the wire.
        """
        self.nodes.append(node)
        if len(self.nodes) > 1:
            self.lengths.append(0)

    def get_total_length(self):
        """
        Returns the total length of the wire.
        """
        return sum(self.lengths)

    def set_color(self, astr):
        """
        Sets the color of the wire.
        """
        self.color = astr

    def get_color(self):
        """
        Gets the color of the wire.
        """
        return self.color

    def set_gauge(self, astr):
        """
        Sets the gauge of the wire.
        """
        self.gauge = astr

    def get_gauge(self):
        """
        Gets the gauge of the wire.
        """
        return self.gauge

    def set_name(self, astr):
        """
        Sets the name of the wire.
        """
        self.name = astr

    def get_name(self):
        """
        Gets the name of the wire.
        """
        return self.name

    def to_dict(self, connectors):
        """
        Returns a dictionary representation of the wire.
        """
        node_data = []
        for node in self.nodes:
            if isinstance(node.parent, Connector):
                node_data.append({
                    "type": "connector",
                    "parent_idx": connectors.index(node.parent),
                    "pin": node.pinnum,
                })
            else:
                node_data.append({
                    "type": "intermediate",
                    "pos": node.rect.center,
                })

        return {
            "name": self.name,
            "partnumber": self.partnumber,
            "color": self.color,
            "gauge": self.gauge,
            "nodes": node_data,
            "lengths": self.lengths,
        }

    @classmethod
    def from_dict(cls, data, connectors):
        """
        Creates a Wire from a dictionary representation.
        """
        wire = cls(
            name=data["name"],
            partnumber=data["partnumber"],
            color=data["color"],
            gauge=data["gauge"],
        )
        wire.lengths = data["lengths"]

        for node_data in data["nodes"]:
            if node_data["type"] == "connector":
                parent = connectors[node_data["parent_idx"]]
                node = parent.nodes[node_data["pin"]]
                wire.add_node(node)
            else:
                node = Node(node_data["pos"], wire, 0, 0)
                wire.add_node(node)

        return wire
