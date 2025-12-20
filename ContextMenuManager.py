"""
This module defines the context menu manager for the HarnessIT application.
"""

import tkinter as tk

class ContextMenuManager:
    """
    Manages the creation and display of context-sensitive menus.
    """
    def __init__(self, app):
        """
        Initializes the ContextMenuManager.

        Args:
            app: The main application instance.
        """
        self.app = app
        self.menu = None

    def show_menu(self, event, obj_type, obj):
        """
        Shows the context menu for the given object type.

        Args:
            event: The event that triggered the menu.
            obj_type (str): The type of the object under the cursor.
            obj: The object under the cursor.
        """
        if self.menu:
            self.menu.destroy()

        self.menu = tk.Menu(self.app.root, tearoff=0)

        if obj_type == "connector":
            self.menu.add_command(label="Copy", command=lambda: self.app.copy())
            self.menu.add_command(label="Delete", command=lambda: self.app.delete_object(obj))
            self.menu.add_command(label="Flip", command=lambda: self.app.flip_object(obj))
        elif obj_type == "wire_node":
            wire = obj.parent
            self.menu.add_command(label="Add Node", command=lambda: self.app.add_node_to_wire(wire, event.x, event.y))
            self.menu.add_command(label="Delete Wire", command=lambda: self.app.delete_object(wire))
        elif obj_type is None:
            self.menu.add_command(label="Paste", command=self.app.paste)
            self.menu.add_command(label="Add Wire", command=self.app.wire_mode)
            self.menu.add_command(label="Add Connector", command=self.app.add_mode)

        self.menu.post(event.x_root, event.y_root)

    def hide_menu(self, event=None):
        """
        Hides the context menu.
        """
        if self.menu:
            self.menu.destroy()
            self.menu = None
