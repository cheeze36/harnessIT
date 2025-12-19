"""
The main window for the HarnessIT application.

This module contains the main application class, `HarnessITWindow`, which manages the user interface,
event handling, and overall application state.
"""

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import HarnessDrawFrame
import HarnessITRibbon
import HarnessComponentProperties
import HarnessComponents
import HarnessConnectorLibrary
import csv
import json
from UndoManager import UndoManager, MoveAction, CreateAction, DeleteAction, FlipAction


class HarnessITWindow():
    """
    The main window for the HarnessIT application.

    This class is responsible for creating and managing the main application window,
    including the menu bar, toolbar, drawing canvas, and property editor. It also
    handles user input, manages the application state, and coordinates the various
    components of the application.
    """
    def __init__(self):
        """
        Initializes the HarnessITWindow.
        """
        self.root = tk.Tk()
        self.root.wm_title("HarnessIT")
        self.root.wm_geometry("800x640")
        self.states = ["normal","adding","selecting","wire", "moving"]
        self.state = "selecting"
        self.undo_manager = UndoManager()
        self.HarnessComponents = HarnessComponents

        with open('resources/library/Connectors.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            self.library = [row for row in csv_reader]

        self.curConAdd = {} # the current connector selection from the library is stored here

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_harness)
        self.filemenu.add_command(label="Open", command=self.open_harness, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save", command=self.save_harness, accelerator="Ctrl+S")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.editmenu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Shift+Z")
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

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
        self.cutlistdata = {}


        self.ribbon = HarnessITRibbon.Ribbon(self.root,self)

        self.sideFrame.grid(column=0,row=0)
        self.HDF.frame.grid(column=1,row=0)
        self.ConnPropFrame.frame.grid(column=0,row=0)
        #self.ribbon.frame.pack(side = tk.TOP)
        self.ribbon.frame.place(x=10,y=10)
        self.tabControl.place(relx=.01,y=40,relheight=.97,relwidth=.99)
        #self.tabControl.pack(expand = 1, fill="both", side = tk.BOTTOM)

        self.status_var = tk.StringVar(value="")
        self.status = ttk.Label(self.root, textvariable=self.status_var, anchor="w")
        self.status.place(relx=0.01, rely=0.975, relwidth=0.98)

        self._dragging = False
        self._drag_action_data = None
        self._drag_offset = (0, 0)

        self.root.bind('<Configure>', self.resize)
        
        self.running = False
        self._bind_input()
        self._set_mode("selecting")


    def _bind_input(self):
        """
        Binds all user input events to their respective handlers.
        """
        # Mouse on the drawing frame
        self.HDF.frame.bind("<Button-1>", self._on_left_click)
        self.HDF.frame.bind("<B1-Motion>", self._on_drag)
        self.HDF.frame.bind("<ButtonRelease-1>", self._on_left_release)
        self.HDF.frame.bind("<Button-3>", self._on_right_click)

        # Keyboard shortcuts (single keys)
        self.root.bind_all("<Escape>", self._cancel_mode)
        self.root.bind_all("<Delete>", self._delete_selection)
        self.root.bind_all("<BackSpace>", self._delete_selection)

        self.root.bind_all("a", self.add_mode)
        self.root.bind_all("w", self.wire_mode)
        self.root.bind_all("s", self.select_mode)
        self.root.bind_all("f", self.flip)
        self.root.bind_all("m", self.move_mode)

        self.root.bind_all("<Control-l>", self.openLibrary)
        self.root.bind_all("<Control-z>", self.undo)
        self.root.bind_all("<Control-Shift-Z>", self.redo)
        self.root.bind_all("<Control-s>", self.save_harness)
        self.root.bind_all("<Control-o>", self.open_harness)


    def _set_status(self, text):
        """
        Sets the text of the status bar.

        Args:
            text (str): The text to display in the status bar.
        """
        self.status_var.set(text)

    def _set_mode(self, mode):
        """
        Sets the application's current mode.

        Args:
            mode (str): The mode to set.
        """
        self.state = mode
        if mode == "selecting":
            self.root.config(cursor="arrow")
            self._set_status(
                "Select: click to select • drag to move • Delete removes • W=Wire • A=Add • F=Flip • Esc=Cancel")
        elif mode == "wire":
            self.root.config(cursor="spider")
            self._set_status("Wire: click 2 pins to connect • right-click or Esc cancels • S=Select")
        elif mode == "adding":
            self.root.config(cursor="plus")
            self._set_status("Add: click to place connector • right-click or Esc cancels • S=Select")
        elif mode == "moving":
            self.root.config(cursor="fleur")
            self._set_status("Move: Click and drag a selected item to move it. Esc to cancel.")
        else:
            self.root.config(cursor="arrow")
            self._set_status("")

    def _cancel_mode(self, event=None):
        """
        Cancels the current mode and returns to the default 'selecting' mode.
        """
        self.wirenodes.clear()
        self._dragging = False
        self._set_mode("selecting")

    def _select_connector(self, obj):
        """
        Selects a connector and displays its properties.

        Args:
            obj (Connector): The connector to select.
        """
        self.properties.frame.grid_forget()
        self.properties = self.ConnPropFrame
        self.properties.frame.grid(column=0, row=0)
        self.HDF.selected.clear()
        self.HDF.selected.append(obj)
        self.properties.load(obj)

    def _select_wire_node(self, node):
        """
        Selects a wire node and displays its properties.

        Args:
            node (Node): The wire node to select.
        """
        self.properties.frame.grid_forget()
        self.properties = self.WirePropFrame
        self.properties.frame.grid(column=0, row=0)
        self.HDF.selected.clear()
        self.HDF.selected.append(node)
        self.properties.load(node)

    def _hit_test(self, x, y):
        """
        Checks if a point collides with any object on the canvas.

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            tuple: A tuple containing the type of object and the object itself, or (None, None) if no object is hit.
        """
        # Check selected first for moving
        if self.state == "moving":
            for obj in self.HDF.selected:
                if obj.rect.collidepoint(x, y):
                    return ("selected", obj)

        for obj in reversed(self.HDF.connectors):
            if obj.rect.collidepoint(x, y):
                return ("connector", obj)

        for w in self.HDF.wires:
            if w.nodeB and w.nodeB.rect.collidepoint(x, y):
                return ("wire_node", w.nodeB)
            if w.nodeC and w.nodeC.rect.collidepoint(x, y):
                return ("wire_node", w.nodeC)

        for obj in self.HDF.connectors:
            for n in obj.nodes:
                if n.rect.collidepoint(x, y):
                    return ("pin_node", n)

        return (None, None)

    def _on_left_click(self, event):
        """
        Handles left-click events on the drawing canvas.
        """
        x, y = event.x, event.y

        if self.state == "adding":
            self.add_connector(event)
            return

        if self.state == "wire":
            self.add_wire(event)
            return

        kind, obj = self._hit_test(x, y)

        if self.state == "moving":
            if kind == "selected":
                self._dragging = True
                self._drag_offset = (obj.rect.centerx - x, obj.rect.centery - y)
                self._drag_action_data = (obj, obj.rect.center)
            return

        if kind == "connector":
            if obj not in self.HDF.selected:
                self._select_connector(obj)
            self._dragging = True
            self._drag_offset = (obj.rect.centerx - x, obj.rect.centery - y)
            self._drag_action_data = (obj, obj.rect.center)
        elif kind == "wire_node":
            if obj not in self.HDF.selected:
                self._select_wire_node(obj)
            self._dragging = True
            self._drag_offset = (obj.rect.centerx - x, obj.rect.centery - y)
            self._drag_action_data = (obj, obj.rect.center)
        elif kind == "pin_node" and self.state == "wire":
             self.add_wire(event)
        else:
            self.HDF.selected.clear()
            self.properties.frame.grid_forget()


    def _on_drag(self, event):
        """
        Handles drag events on the drawing canvas.
        """
        if self.state not in ["selecting", "moving"]:
            return
        if not self._dragging:
            return
        if not self.HDF.selected:
            return

        sel = self.HDF.selected[0]
        # Check if sel is a valid object with a rect attribute
        if not hasattr(sel, 'rect'):
            return

        dx, dy = self._drag_offset
        sel.rect.center = (event.x + dx, event.y + dy)

    def _on_left_release(self, event):
        """
        Handles left-click release events on the drawing canvas.
        """
        if self._dragging and self._drag_action_data:
            obj, old_pos = self._drag_action_data
            new_pos = obj.rect.center
            if old_pos != new_pos:
                action = MoveAction(obj, old_pos, new_pos)
                self.undo_manager.register(action)
        self._dragging = False
        self._drag_action_data = None


    def _on_right_click(self, event):
        """
        Handles right-click events on the drawing canvas.
        """
        self._cancel_mode()

    def _delete_selection(self, event=None):
        """
        Deletes the currently selected object.
        """
        if not self.HDF.selected:
            return

        sel = self.HDF.selected[0]
        action = DeleteAction(self, sel)
        self.undo_manager.register(action)
        
        if isinstance(sel, HarnessComponents.Connector):
            if sel in self.HDF.connectors:
                self.HDF.connectors.remove(sel)
        elif isinstance(sel, HarnessComponents.Node):
            parent = getattr(sel, "parent", None)
            if parent and parent in self.HDF.wires:
                self.HDF.wires.remove(parent)

        self.HDF.selected.clear()

    def add_mode(self, *args):
        """
        Enters 'adding' mode, allowing the user to add new connectors.
        """
        if len(self.curConAdd) > 0:
            self._set_mode("adding")
        else:
            self.openLibrary(callback=self.add_mode)

    def add_connector(self,event):
        """
        Adds a new connector to the canvas.
        """
        connector = HarnessComponents.Connector(self.curConAdd["ImageLocation"],(event.x,event.y),connections=self.curConAdd["Positions"])
        self.HDF.connectors.append(connector)
        action = CreateAction(self, connector)
        self.undo_manager.register(action)
        self._set_mode("selecting")

    def openLibrary(self, *args, callback=None):
        """
        Opens the connector library window.
        """
        if self.libwin:
            self.libwin.window.lift()
            return
        self.libwin = HarnessConnectorLibrary.ConnectorLibrary(self.root, self, callback=callback)

    def set_current(self,concard):
        """
        Sets the current connector to be added from the library.
        """
        for i in self.library:
            if concard == i["ID"]:
                self.curConAdd = i
        
        if self.libwin:
            if self.libwin.callback:
                self.libwin.callback()
            self.libwin.window.destroy()
            self.libwin = None
        
    def remove(self, *args):
        """
        Removes the currently selected object.
        """
        self._delete_selection()

    def select_mode(self, *args):
        """
        Enters 'selecting' mode.
        """
        self._set_mode("selecting")

    def generate_cutlist(self,*args):
        """
        Generates and displays the cut list for the current harness.
        """
        self.tabControl.select(self.tabControl.index(1))
        
        for i in self.CutListEditTab.winfo_children():
            i.destroy()

        row = 1
        for w in self.HDF.wires:
            left = w.nodeA.get_name()
            leftentry = tk.Entry(self.CutListEditTab, width=20)
            leftentry.insert(0,left)
            leftentry.grid(row = row,column=0)
            wirename = w.name
            nameentry = tk.Entry(self.CutListEditTab, width=20)
            nameentry.insert(0, wirename)
            nameentry.grid(row=row, column=1)
            right = w.nodeD.get_name()
            rightentry = tk.Entry(self.CutListEditTab, width=20)
            rightentry.insert(0, right)
            rightentry.grid(row=row, column=2)
            row +=1

    def wire_mode(self,*args):
        """
        Enters 'wire' mode, allowing the user to add new wires.
        """
        self._set_mode("wire")

    def add_wire(self,event,*args):
        """
        Adds a new wire to the canvas.
        """
        kind, obj = self._hit_test(event.x, event.y)
        if kind == "pin_node":
            if obj in self.wirenodes:
                self.wirenodes.remove(obj)
            else:
                self.wirenodes.append(obj)
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
                    action = CreateAction(self, w)
                    self.undo_manager.register(action)
                    self.wirenodes.clear()
                    self._set_mode("selecting")

    def move_mode(self, *args):
        """
        Enters 'moving' mode, allowing the user to move selected objects.
        """
        self._set_mode("moving")
        
    def flip(self,*args):
        """
        Flips the currently selected connector.
        """
        if len(self.HDF.selected) > 0:
            sel = self.HDF.selected[0]
            sel.flip()
            action = FlipAction(sel)
            self.undo_manager.register(action)

    def resize(self,*args):
        """
        Resizes the drawing canvas.
        """
        self.HDF.resize()

    def undo(self, event=None):
        """
        Undoes the last action.
        """
        self.undo_manager.undo()

    def redo(self, event=None):
        """
        Redoes the last undone action.
        """
        self.undo_manager.redo()

    def new_harness(self):
        """
        Clears the current harness and starts a new one.
        """
        self.HDF.connectors.clear()
        self.HDF.wires.clear()
        self.undo_manager.clear()

    def save_harness(self, event=None):
        """
        Saves the current harness to a file.
        """
        filepath = filedialog.asksaveasfilename(
            defaultextension="json",
            filetypes=[("Harness Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return

        harness_data = {
            "connectors": [c.to_dict() for c in self.HDF.connectors],
            "wires": [w.to_dict(self.HDF.connectors) for w in self.HDF.wires],
        }

        with open(filepath, "w") as f:
            json.dump(harness_data, f, indent=4)

    def open_harness(self, event=None):
        """
        Opens a harness from a file.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("Harness Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "r") as f:
            harness_data = json.load(f)

        self.new_harness()
        
        for c_data in harness_data["connectors"]:
            connector = HarnessComponents.Connector.from_dict(c_data)
            self.HDF.connectors.append(connector)

        for w_data in harness_data["wires"]:
            wire = HarnessComponents.Wire.from_dict(w_data, self.HDF.connectors)
            self.HDF.wires.append(wire)

    def Run(self):
        """
        Starts the main application loop.
        """
        self.running = True
        while self.running:
            self.HDF.draw()
            self.HDF.update()
            self.root.update()

myApp = HarnessITWindow()
myApp.Run()
