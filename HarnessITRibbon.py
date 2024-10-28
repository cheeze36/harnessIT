import tkinter as tk
import tkinter.ttk as ttk
import tktooltip

class Ribbon():
    def __init__(self, parent, app):
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


        #load buttons
        self.addConnectorButton = ttk.Button(self.frame, text = "Add Connector", image=self.addConnectorImage,command=self.app.add_mode)
        #self.addConnectorButton.grid(column=0,row=0)
        self.addConnectorButton.pack(side=tk.LEFT)
        tktooltip.ToolTip(self.addConnectorButton, "add connector", 1)

        self.addWireButton = ttk.Button(self.frame, text="Add Wire", image=self.addWireImage, command=self.app.wire_mode)
        #self.addWireButton.grid(column=1, row=0)
        self.addWireButton.pack(side=tk.LEFT)
        tktooltip.ToolTip(self.addWireButton, "add wire", 1)

        self.removeConnectorButton = ttk.Button(self.frame, text="Add Connector", image=self.removeConnectorImage,command=self.app.remove)
        #self.addConnectorButton.grid(column=2, row=0)
        self.removeConnectorButton.pack(side=tk.LEFT)
        tktooltip.ToolTip(self.removeConnectorButton, "remove connector", 1)

        self.selectButton = ttk.Button(self.frame, text = "Select", image =self.selectImage,command=self.app.select_mode)
        self.selectButton.pack(side=tk.LEFT)
        tktooltip.ToolTip(self.selectButton, "select", 1)

        self.openLibraryButton = ttk.Button(self.frame, text = "Open Library", image=self.openLibraryimage,command=self.app.openLibrary)
        self.openLibraryButton.pack(side=tk.LEFT)
        tktooltip.ToolTip(self.openLibraryButton,"Open Library",1)

        self.flipConnectorButton = ttk.Button(self.frame, text = "Flip Connector", image = self.flipConnectorImage,command=self.app.flip)
        self.flipConnectorButton.pack(side="left")
        tktooltip.ToolTip(self.flipConnectorButton,"Flip Button",1)




