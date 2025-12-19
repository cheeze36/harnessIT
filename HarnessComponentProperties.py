"""
This module defines the property editor panels for connectors and wires.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tktooltip
import HarnessITUtils

class ConnectorProperies():
    """
    A property editor panel for connectors.
    """
    def __init__(self, parent, app):
        """
        Initializes the ConnectorProperies panel.

        Args:
            parent: The parent widget.
            app: The main application instance.
        """
        self.app = app
        self.parent = parent
        self.frame = tk.Frame(self.parent, height=200)

        self.titleLabel = ttk.Label(self.frame, text="Connector prop.")
        self.titleLabel.grid(column=0, row=0, sticky="n")

        self.nameLabel = ttk.Label(self.frame,text="Name")
        self.nameLabel.grid(column=0,row=1,sticky = "n")
        self.nameTextBox = ttk.Entry(self.frame,width=20)
        self.nameTextBox.grid(column=0,row=2,sticky = "n")

        self.partNumberlabel = ttk.Label(self.frame,text = "part number")
        self.partNumberlabel.grid(column=0, row=3, sticky="n")
        self.partNumberTextBox =ttk.Entry(self.frame,width=20)
        self.partNumberTextBox.grid(column=0, row=4, sticky="n")


        self.saveButton = ttk.Button(self.frame,text = "save", command = self.save)
        self.saveButton.grid(column=0,row=10,columnspan=2)

    def load(self, component):
        """
        Loads the properties of a connector into the panel.

        Args:
            component (Connector): The connector to load.
        """
        self.nameTextBox.delete(0,30)
        self.nameTextBox.insert(0,component.get_name())
        self.partNumberTextBox.delete(0,30)
        self.partNumberTextBox.insert(0, component.partNumber)


    def save(self):
        """
        Saves the properties of the connector.
        """
        if len(self.app.HDF.selected) > 0:
            self.app.HDF.selected[0].set_name(self.nameTextBox.get())
            print("saved")
class WireProperies():
    """
    A property editor panel for wires.
    """
    def __init__(self, parent, app):
        """
        Initializes the WireProperies panel.

        Args:
            parent: The parent widget.
            app: The main application instance.
        """
        self.app = app
        self.parent = parent
        self.frame = tk.Frame(self.parent, height=200)

        self.titleLabel = ttk.Label(self.frame, text="Wire prop.")
        self.titleLabel.grid(column=0, row=0, sticky="n")

        self.nameLabel = ttk.Label(self.frame,text="Name")
        self.nameLabel.grid(column=0,row=1,sticky = "n")
        self.nameTextBox = ttk.Entry(self.frame,width=20)
        self.nameTextBox.grid(column=0,row=2,sticky = "n")

        self.partNumberlabel = ttk.Label(self.frame,text = "part number")
        self.partNumberlabel.grid(column=0, row=3, sticky="n")
        self.partNumberTextBox =ttk.Entry(self.frame,width=20)
        self.partNumberTextBox.grid(column=0, row=4, sticky="n")

        self.colorLabel = ttk.Label(self.frame, text="color")
        self.colorLabel.grid(column=0, row=5, sticky="n")

        self.colorChooser = ttk.Combobox(self.frame, state= "readonly", values=list(HarnessITUtils.COLORS.keys()))
        self.colorChooser.grid(column=0, row=6, sticky="n")

        self.gaugeLabel = ttk.Label(self.frame, text="Gauge")
        self.gaugeLabel.grid(column=0, row=7, sticky="n")
        self.gaugeChooser = ttk.Combobox(self.frame, state= "readonly", values=list(HarnessITUtils.GAUGE.keys()))
        self.gaugeChooser.grid(column=0, row=8, sticky="n")


        self.saveButton = ttk.Button(self.frame,text = "save", command = self.save)
        self.saveButton.grid(column=0,row=10,columnspan=2)

    def load(self, component):
        """
        Loads the properties of a wire into the panel.

        Args:
            component (Wire): The wire to load.
        """
        self.nameTextBox.delete(0,30)
        self.nameTextBox.insert(0,component.get_name())
        #self.partNumberTextBox.delete(0,30)
        #self.partNumberTextBox.insert(0, component.partNumber)
        self.colorChooser.set(value=component.get_color())
        self.gaugeChooser.set(value=component.get_gauge())


    def save(self):
        """
        Saves the properties of the wire.
        """
        if len(self.app.HDF.selected) > 0:
            self.app.HDF.selected[0].set_name(self.nameTextBox.get())
            print("saved")
            self.app.HDF.selected[0].set_color(self.colorChooser.get())
            self.app.HDF.selected[0].set_gauge(self.gaugeChooser.get())
