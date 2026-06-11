"""
This module defines the ribbon toolbar for the HarnessIT application.
"""

import tkinter as tk
import tkinter.ttk as ttk
try:
    import TkToolTip as tktooltip
except Exception:
    tktooltip = None

class Ribbon():
    """
    The ribbon toolbar for the HarnessIT application.
    """
    def __init__(self, parent, app):
        """
        Initializes the Ribbon.

        Args:
            parent: The parent widget.
            app: The main application instance.
        """
        self.app = app
        self.parent = parent
        self.frame = tk.Frame(self.parent, height= 50)

        #load images
        self.addConnectorImage = tk.PhotoImage(file= "resources/images/add_connector.png")
        self.addWireImage = tk.PhotoImage(file= "resources/images/add_wire.png")
        self.removeConnectorImage = tk.PhotoImage(file="resources/images/remove_connector.png")
        self.selectImage = tk.PhotoImage(file="resources/images/select.png")
        self.openLibraryimage = tk.PhotoImage(file = "resources/images/library.png")
        self.flipConnectorImage = tk.PhotoImage(file = "resources/images/flip.png")
        self.cutsheetImage = tk.PhotoImage(file="resources/images/cutlist.png")
        self.moveImage = tk.PhotoImage(file="resources/images/select.png")


        #load buttons
        self.addConnectorButton = ttk.Button(self.frame, text = "Add Connector", image=self.addConnectorImage,command=self.app.add_mode)
        self.addConnectorButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.addConnectorButton, text="add connector")

        self.addWireButton = ttk.Button(self.frame, text="Add Wire", image=self.addWireImage, command=self.app.wire_mode)
        self.addWireButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.addWireButton, text="add wire")

        self.removeConnectorButton = ttk.Button(self.frame, text="Add Connector", image=self.removeConnectorImage,command=self.app.remove)
        self.removeConnectorButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.removeConnectorButton, text="remove connector")

        self.selectButton = ttk.Button(self.frame, text = "Select", image =self.selectImage,command=self.app.select_mode)
        self.selectButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.selectButton, text="select")

        self.moveButton = ttk.Button(self.frame, text="Move", image=self.moveImage, command=self.app.move_mode)
        self.moveButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.moveButton, text="Move Selected")

        self.openLibraryButton = ttk.Button(self.frame, text = "Open Library", image=self.openLibraryimage,command=self.app.openLibrary)
        self.openLibraryButton.pack(side=tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.openLibraryButton, text="Open Library")

        self.flipConnectorButton = ttk.Button(self.frame, text = "Flip Connector", image = self.flipConnectorImage,command=self.app.flip)
        self.flipConnectorButton.pack(side="left")
        if tktooltip:
            tktooltip.ToolTip(self.flipConnectorButton, text="Flip Button")

        self.generateCutsheetButton = ttk.Button(self.frame, text = "generate Cutsheet", image = self.cutsheetImage, command = self.app.generate_cutlist)
        self.generateCutsheetButton.pack(side = tk.LEFT)
        if tktooltip:
            tktooltip.ToolTip(self.generateCutsheetButton, text="generate cutsheet")
