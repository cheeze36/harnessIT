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
from UndoManager import UndoManager, MoveAction, CreateAction, DeleteAction, FlipAction, CopyAction, PasteAction
from ContextMenuManager import ContextMenuManager


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
        self.clipboard = None
        self.context_menu_manager = ContextMenuManager(self)

        self.grid_visible = tk.BooleanVar(value=True)
        self.grid_snap = tk.BooleanVar(value=True)
        self.grid_size = 25

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
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.editmenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.gridmenu = tk.Menu(self.menubar, tearoff=0)
        self.gridmenu.add_checkbutton(label="Show Grid", onvalue=True, offvalue=False, variable=self.grid_visible)
        self.gridmenu.add_checkbutton(label="Snap to Grid", onvalue=True, offvalue=False, variable=self.grid_snap)
        self.menubar.add_cascade(label="Grid", menu=self.gridmenu)

        self.windowmenu = tk.Menu(self.menubar, tearoff=0)
        self.windowmenu.add_command(label="Connector Library", command=self.openLibrary)
        self.windowmenu.add_command(label="Cut List", command=self.generate_cutlist)
        self.menubar.add_cascade(label="Window", menu=self.windowmenu)


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
        self.HDF.frame.bind("<Control-MouseWheel>", self.HDF.zoom)


        # Keyboard shortcuts (single keys)
        self.root.bind_all("<Escape>", self._cancel_mode)
        self.root.bind_all("<Delete>", self._delete_selection)
        #self.root.bind_all("<BackSpace>", self._delete_selection)

        self.root.bind_all("<Control-a>", self.select_all)
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
        self.root.bind_all("<Control-c>", self.copy)
        self.root.bind_all("<Control-v>", self.paste)


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
        from HarnessComponents import Connector
        if isinstance(node.parent, Connector):
            self._select_connector(node.parent)
            return

        self.properties.frame.grid_forget()
        self.properties = self.WirePropFrame
        self.properties.frame.grid(column=0, row=0)
        self.HDF.selected.clear()
        self.HDF.selected.append(node)
        self.properties.load(node.parent)

    def _hit_test(self, x, y):
        """
        Checks if a point collides with any object on the canvas.

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            tuple: A tuple containing the type of object and the object itself, or (None, None) if no object is hit.
        """
        world_x, world_y = self.HDF.screen_to_world(x, y)

        # Check selected first for moving
        if self.state == "moving":
            for obj in self.HDF.selected:
                if obj.rect.collidepoint(world_x, world_y):
                    return ("selected", obj)

        for obj in reversed(self.HDF.connectors):
            if obj.rect.collidepoint(world_x, world_y):
                return ("connector", obj)

        for w in self.HDF.wires:
            for node in w.nodes:
                if node.rect.collidepoint(world_x, world_y):
                    return ("wire_node", node)

        for obj in self.HDF.connectors:
            for n in obj.nodes:
                if n.rect.collidepoint(world_x, world_y):
                    return ("pin_node", n)

        return (None, None)

    def _on_left_click(self, event):
        """
        Handles left-click events on the drawing canvas.
        """
        self.context_menu_manager.hide_menu()
        x, y = event.x, event.y
        world_x, world_y = self.HDF.screen_to_world(x, y)

        if self.grid_snap.get():
            world_x, world_y = self.HDF.snap_to_grid(world_x, world_y)

        if self.state == "adding":
            self.add_connector(world_x, world_y)
            return

        if self.state == "wire":
            self.add_wire(event)
            return

        kind, obj = self._hit_test(x, y)

        if self.state == "moving":
            if kind == "selected":
                self._dragging = True
                self._drag_offset = (obj.rect.centerx - world_x, obj.rect.centery - world_y)
                self._drag_action_data = (obj, obj.rect.center)
            return

        if kind == "connector":
            if obj not in self.HDF.selected:
                self._select_connector(obj)
            self._dragging = True
            self._drag_offset = (obj.rect.centerx - world_x, obj.rect.centery - world_y)
            self._drag_action_data = (obj, obj.rect.center)
        elif kind == "wire_node":
            if obj not in self.HDF.selected:
                self._select_wire_node(obj)
            self._dragging = True
            self._drag_offset = (obj.rect.centerx - world_x, obj.rect.centery - world_y)
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

        world_x, world_y = self.HDF.screen_to_world(event.x, event.y)
        dx, dy = self._drag_offset
        
        new_x = world_x + dx
        new_y = world_y + dy

        if self.grid_snap.get():
            new_x, new_y = self.HDF.snap_to_grid(new_x, new_y)

        sel.rect.center = (new_x, new_y)

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
        kind, obj = self._hit_test(event.x, event.y)
        self.context_menu_manager.show_menu(event, kind, obj)

    def _delete_selection(self, event=None):
        """
        Deletes the currently selected object.
        """
        if not self.HDF.selected:
            return

        sel = self.HDF.selected[0]
        self.delete_object(sel)

    def delete_object(self, obj):
        """
        Deletes a specific object.
        """
        action = DeleteAction(self, obj)
        self.undo_manager.register(action)
        
        if isinstance(obj, HarnessComponents.Connector):
            if obj in self.HDF.connectors:
                self.HDF.connectors.remove(obj)
        elif isinstance(obj, HarnessComponents.Wire):
            if obj in self.HDF.wires:
                self.HDF.wires.remove(obj)
        elif isinstance(obj, HarnessComponents.Node):
            parent = getattr(obj, "parent", None)
            if parent and parent in self.HDF.wires:
                self.HDF.wires.remove(parent)

        if obj in self.HDF.selected:
            self.HDF.selected.remove(obj)

    def flip_object(self, obj):
        """
        Flips a specific connector.
        """
        if isinstance(obj, HarnessComponents.Connector):
            obj.flip()
            action = FlipAction(obj)
            self.undo_manager.register(action)

    def add_node_to_wire(self, wire, x, y):
        """
        Adds a new node to a wire at the given position.
        """
        world_x, world_y = self.HDF.screen_to_world(x, y)
        if self.grid_snap.get():
            world_x, world_y = self.HDF.snap_to_grid(world_x, world_y)

        # Find the closest segment to the click
        min_dist = float('inf')
        insert_index = -1
        for i in range(len(wire.nodes) - 1):
            p1 = pygame.math.Vector2(wire.nodes[i].rect.center)
            p2 = pygame.math.Vector2(wire.nodes[i+1].rect.center)
            p3 = pygame.math.Vector2(world_x, world_y)
            dist = p3.distance_to(p1) + p3.distance_to(p2)
            if dist < min_dist:
                min_dist = dist
                insert_index = i + 1
        
        if insert_index != -1:
            node = HarnessComponents.Node((world_x, world_y), wire, 0, 0)
            wire.nodes.insert(insert_index, node)
            wire.lengths.insert(insert_index - 1, 0)
            self.properties.load(wire)


    def add_mode(self, *args):
        """
        Enters 'adding' mode, allowing the user to add new connectors.
        """
        if len(self.curConAdd) > 0:
            self._set_mode("adding")
        else:
            self.openLibrary(callback=self.add_mode)

    def add_connector(self, x, y):
        """
        Adds a new connector to the canvas.
        """
        connector = HarnessComponents.Connector(self.curConAdd["ImageLocation"],(x,y),connections=self.curConAdd["Positions"])
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

    def select_all(self, *args):
        """
        Selects all connectors and wires in the harness.
        """
        self.HDF.selected.clear()
        self.HDF.selected.extend(self.HDF.connectors)
        # Optionally add wires if you want them selected too
        # self.HDF.selected.extend(self.HDF.wires)

    def generate_cutlist(self,*args):
        """
        Generates and displays the cut list for the current harness.
        """
        self.tabControl.select(self.tabControl.index(1))
        
        for i in self.CutListEditTab.winfo_children():
            i.destroy()

        row = 1
        for w in self.HDF.wires:
            left = w.nodes[0].get_name()
            leftentry = tk.Entry(self.CutListEditTab, width=20)
            leftentry.insert(0,left)
            leftentry.grid(row = row,column=0)
            wirename = w.name
            nameentry = tk.Entry(self.CutListEditTab, width=20)
            nameentry.insert(0, wirename)
            nameentry.grid(row=row, column=1)
            length = w.get_total_length()
            length_entry = tk.Entry(self.CutListEditTab, width=10)
            length_entry.insert(0, str(length))
            length_entry.grid(row=row, column=2)
            right = w.nodes[-1].get_name()
            rightentry = tk.Entry(self.CutListEditTab, width=20)
            rightentry.insert(0, right)
            rightentry.grid(row=row, column=3)
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
                    w.add_node(self.wirenodes[0])
                    
                    # Add two intermediate nodes
                    start_pos = self.wirenodes[0].rect.center
                    end_pos = self.wirenodes[1].rect.center
                    
                    x_dist = (end_pos[0] - start_pos[0]) / 3
                    y_dist = (end_pos[1] - start_pos[1]) / 3

                    pos1 = (start_pos[0] + x_dist, start_pos[1] + y_dist)
                    pos2 = (start_pos[0] + 2 * x_dist, start_pos[1] + 2 * y_dist)

                    node1 = HarnessComponents.Node(pos1, w, 0, 0)
                    node2 = HarnessComponents.Node(pos2, w, 0, 0)

                    w.add_node(node1)
                    w.add_node(node2)
                    w.add_node(self.wirenodes[1])

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
            self.flip_object(sel)

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

    def copy(self, event=None):
        """
        Copies the selected objects to the clipboard.
        """
        if not self.HDF.selected:
            return
        
        action = CopyAction(self)
        action.execute()
        self.clipboard = action.clipboard_data

    def paste(self, event=None):
        """
        Pastes the objects from the clipboard to the canvas.
        """
        if not self.clipboard:
            return

        pasted_objects = self.paste_selection(self.clipboard)
        action = PasteAction(self, pasted_objects)
        self.undo_manager.register(action)

    def copy_selection(self):
        """
        Serializes the selected objects to a clipboard-friendly format.
        """
        if not self.HDF.selected:
            return None

        clipboard_data = {
            "connectors": [],
            "wires": [],
        }

        selected_connectors = [obj for obj in self.HDF.selected if isinstance(obj, HarnessComponents.Connector)]
        
        for c in selected_connectors:
            clipboard_data["connectors"].append(c.to_dict())

        selected_wires = []
        for obj in self.HDF.selected:
            if isinstance(obj, HarnessComponents.Node) and isinstance(obj.parent, HarnessComponents.Wire):
                if obj.parent not in selected_wires:
                    selected_wires.append(obj.parent)
        
        for w in selected_wires:
            clipboard_data["wires"].append(w.to_dict(self.HDF.connectors))

        return clipboard_data

    def paste_selection(self, clipboard_data):
        """
        Pastes the objects from the clipboard to the canvas.
        """
        pasted_objects = []
        new_connectors = []
        
        for c_data in clipboard_data["connectors"]:
            c_data["pos"] = (c_data["pos"][0] + 20, c_data["pos"][1] + 20)
            connector = HarnessComponents.Connector.from_dict(c_data)
            self.HDF.connectors.append(connector)
            new_connectors.append(connector)
            pasted_objects.append(connector)

        for w_data in clipboard_data["wires"]:
            wire = HarnessComponents.Wire.from_dict(w_data, self.HDF.connectors)
            self.HDF.wires.append(wire)
            pasted_objects.append(wire)
            
        return pasted_objects


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
