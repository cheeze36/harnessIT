import tkinter as tk
import tkinter.ttk as ttk
import pygame
import HarnessDrawFrame
import HarnessITRibbon
import HarnessComponentProperties
import HarnessComponents
import HarnessConnectorLibrary
import csv

"""
Class: HarnessITWindow()
Author: Christopher Eldridge
Purpose: The main window for the application

list of methods
add_mode(*args)
add_connector(

"""
class HarnessITWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("HarnessIT")
        self.root.wm_geometry("800x640")
        self.states = ["normal","adding","selecting","wire"]
        self.state = "normal"
        with open('resources/library/Connectors.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            self.library = [row for row in csv_reader]

        self.curConAdd = {} # the current connector selection from the library is stored here

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=lambda :print("cheese"))
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.root.config(menu = self.menubar)

        self.tabControl = ttk.Notebook(self.root)

        self.HarnessEditTab = ttk.Frame(self.tabControl)
        self.CutListEditTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.HarnessEditTab,text = "Harness Edit")
        self.tabControl.add(self.CutListEditTab, text = "Cut list")

        self.HDF = HarnessDrawFrame.DrawFrame(self.HarnessEditTab,self)
        self.sideFrame = tk.Frame(self.HarnessEditTab)
        self.ConnPropFrame = HarnessComponentProperties.ConnectorProperies(self.HarnessEditTab,self)
        self.WirePropFrame = HarnessComponentProperties.WireProperies(self.HarnessEditTab,self)
        self.properties = self.ConnPropFrame

        self.libwin = None
        self.wirenodes = []


        self.ribbon = HarnessITRibbon.Ribbon(self.root,self)

        self.sideFrame.grid(column=0,row=0)
        self.HDF.frame.grid(column=1,row=0)
        self.ConnPropFrame.frame.grid(column=0,row=0)
        #self.ribbon.frame.pack(side = tk.TOP)
        self.ribbon.frame.place(x=10,y=10)
        self.tabControl.place(relx=.01,y=40,relheight=.97,relwidth=.99)
        #self.tabControl.pack(expand = 1, fill="both", side = tk.BOTTOM)


        self.root.bind('<Configure>', self.resize)
        self.root.bind("<Alt-m>", self.move_connector)
        self.root.bind("<Alt-f>", self.move_connector)
        self.root.bind("<Control-a>", self.add_mode)
        self.root.bind("<Control-s>", self.select_mode)

        self.running = False
    def add_mode(self, *args):
        if len(self.curConAdd) > 0:
            self.root.config(cursor="plus")
            self.HDF.frame.bind("<ButtonRelease-1>",self.add_connector)
            self.state = "adding"
        else:
            self.openLibrary()
    def add_connector(self,event):
        self.HDF.connectors.append(HarnessComponents.Connector(self.curConAdd["ImageLocation"],(event.x,event.y),connections=self.curConAdd["Positions"]))
        self.root.config(cursor="arrow")
        self.HDF.frame.unbind("<ButtonRelease-1>")
        self.state = "normal"
    def openLibrary(self,*args):
        self.libwin = HarnessConnectorLibrary.ConnectorLibrary(self.root,self)
    def set_current(self,concard):
        for i in self.library:
            if concard == i["ID"]:
                self.curConAdd = i
        print(concard)
        self.libwin.window.destroy()
        self.libwin = None
        self.add_mode()

    def remove(self):
        if len(self.HDF.selected) > 0:
            self.HDF.connectors.remove(self.HDF.selected[0])
            self.HDF.selected.clear()
    def select_mode(self, *args):
        self.root.config(cursor="cross")
        self.root.bind("<ButtonRelease-1>", self.select)
        self.state = "selecting"
    def select(self,event):
        for obj in self.HDF.connectors:
            if obj.rect.collidepoint(event.x,event.y):
                if obj in self.HDF.selected:
                    self.HDF.selected.remove(obj)
                else:
                    self.properties.frame.grid_forget()
                    self.properties = self.ConnPropFrame
                    self.properties.frame.grid(column=0,row= 0)
                    self.HDF.selected.clear()
                    self.HDF.selected.append(obj)
                    self.properties.load(obj)
        for w in self.HDF.wires:
            if w.nodeB.rect.collidepoint(event.x,event.y):
                if w.nodeB in self.HDF.selected:
                    self.HDF.selected.remove(w.nodeB)
                else:
                    self.properties.frame.grid_forget()
                    self.properties = self.WirePropFrame
                    self.properties.frame.grid(column=0, row=0)
                    self.HDF.selected.clear()
                    self.HDF.selected.append(w.nodeB)
                    self.properties.load(w.nodeB)
            if w.nodeC.rect.collidepoint(event.x,event.y):
                if w.nodeC in self.HDF.selected:
                    self.HDF.selected.remove(w.nodeC)
                else:
                    self.properties.frame.grid_forget()
                    self.properties = self.WirePropFrame
                    self.properties.frame.grid(column=0, row=0)
                    self.HDF.selected.clear()
                    self.HDF.selected.append(w.nodeC)
                    self.properties.load(w.nodeC)

        self.root.config(cursor="arrow")
        self.root.unbind("<ButtonRelease-1>")
        self.state = "normal"
    def generate_cutlist(self,*args):
        self.tabControl.select(self.tabControl.index(1))
        print(self.tabControl.select())
        for w in self.HDF.wires:
            print(w.name)
    def wire_mode(self,*args):
        self.root.config(cursor="spider")
        self.root.bind("<ButtonRelease-1>", self.add_wire)
        self.state = "wire"
    def add_wire(self,event,*args):
        for obj in self.HDF.connectors:
            for n in obj.nodes:
                if n.rect.collidepoint(event.x,event.y):
                    if n in self.wirenodes:
                        self.wirenodes.remove(n)
                    else:
                        self.wirenodes.append(n)
                        if len(self.wirenodes) == 2:
                            w = HarnessComponents.Wire()
                            hp = ((self.wirenodes[0].rect.centerx + self.wirenodes[1].rect.centerx)/ 2,
                                    (self.wirenodes[0].rect.centery + self.wirenodes[1].rect.centery)/ 2)
                            bpos = ((self.wirenodes[0].rect.centerx + hp[0])/ 2,
                                    (self.wirenodes[0].rect.centery + hp[1])/2)
                            b = HarnessComponents.Node(bpos,w,2,0)
                            cpos = ((hp[0] + self.wirenodes[1].rect.centerx) / 2,
                                    (hp[1] + self.wirenodes[1].rect.centery) / 2)
                            c = HarnessComponents.Node(cpos, w, 2, 0)
                            w.set_nodes(self.wirenodes[0],b,c,self.wirenodes[1])
                            self.HDF.wires.append(w)
                            self.wirenodes.clear()
    def move_connector(self, event):
        if len(self.HDF.selected) > 0:
            self.HDF.selected[0].rect.center = (event.x ,event.y )
    def flip(self,*args):
        if len(self.HDF.selected) > 0:
            self.HDF.selected[0].flip()
    def resize(self,*args):
        self.HDF.resize()
    def Run(self):
        self.running = True
        while self.running:
            self.HDF.draw()
            self.HDF.update()
            self.root.update()

myApp = HarnessITWindow()
myApp.Run()

