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

    def flip(self):
        """
        Flips the connector horizontally.
        """
        self.image = pygame.transform.flip(self.image, 1, 0)
        if self.direction == "left":
            self.direction = "right"
        else:
            self.direction = "left"

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
    A wire represents a connection between two nodes.
    """
    def __init__(self, name="??", partnumber="", color="WHITE", gauge="32", length="0"):
        """
        Initializes a Wire.

        Args:
            name (str, optional): The name of the wire. Defaults to "??".
            partnumber (str, optional): The part number of the wire. Defaults to "".
            color (str, optional): The color of the wire. Defaults to "WHITE".
            gauge (str, optional): The gauge of the wire. Defaults to "32".
            length (str, optional): The length of the wire. Defaults to "0".
        """
        self.nodeA = None
        self.nodeB = None
        self.nodeC = None
        self.nodeD = None
        self.name = name
        self.partnumber = partnumber
        self.color = color
        self.gauge = gauge
        self.length = length

    def set_nodes(self, a, b, c, d):
        """
        Sets the nodes that the wire connects.
        """
        self.nodeA = a
        self.nodeB = b
        self.nodeC = c
        self.nodeD = d

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
        return {
            "name": self.name,
            "partnumber": self.partnumber,
            "color": self.color,
            "gauge": self.gauge,
            "length": self.length,
            "nodeA_parent_idx": connectors.index(self.nodeA.parent),
            "nodeA_pin": self.nodeA.pinnum,
            "nodeB_pos": self.nodeB.rect.center,
            "nodeC_pos": self.nodeC.rect.center,
            "nodeD_parent_idx": connectors.index(self.nodeD.parent),
            "nodeD_pin": self.nodeD.pinnum,
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
            length=data["length"],
        )

        nodeA_parent = connectors[data["nodeA_parent_idx"]]
        nodeD_parent = connectors[data["nodeD_parent_idx"]]

        if nodeA_parent and nodeD_parent:
            nodeA = nodeA_parent.nodes[data["nodeA_pin"]]
            nodeD = nodeD_parent.nodes[data["nodeD_pin"]]
            nodeB = Node(data["nodeB_pos"], wire, 0, 0)
            nodeC = Node(data["nodeC_pos"], wire, 0, 0)
            wire.set_nodes(nodeA, nodeB, nodeC, nodeD)

        return wire
