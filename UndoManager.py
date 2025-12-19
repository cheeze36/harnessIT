"""
This module provides an undo/redo framework for the HarnessIT application.
"""

class UndoManager:
    """
    A class that manages undo and redo operations.
    """
    def __init__(self):
        """
        Initializes the UndoManager.
        """
        self.undo_stack = []
        self.redo_stack = []

    def register(self, action):
        """
        Registers an action with the undo manager.

        Args:
            action: The action to register.
        """
        self.undo_stack.append(action)
        self.redo_stack.clear()

    def undo(self):
        """
        Undoes the last action.
        """
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo()
        self.redo_stack.append(action)

    def redo(self):
        """
        Redoes the last undone action.
        """
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.redo()
        self.undo_stack.append(action)

    def clear(self):
        """
        Clears the undo and redo stacks.
        """
        self.undo_stack.clear()
        self.redo_stack.clear()


class MoveAction:
    """
    An action that represents moving an object.
    """
    def __init__(self, obj, old_pos, new_pos):
        """
        Initializes a MoveAction.

        Args:
            obj: The object that was moved.
            old_pos: The original position of the object.
            new_pos: The new position of the object.
        """
        self.obj = obj
        self.old_pos = old_pos
        self.new_pos = new_pos

    def undo(self):
        """
        Undoes the move action.
        """
        self.obj.rect.center = self.old_pos

    def redo(self):
        """
        Redoes the move action.
        """
        self.obj.rect.center = self.new_pos


class CreateAction:
    """
    An action that represents creating an object.
    """
    def __init__(self, app, obj):
        """
        Initializes a CreateAction.

        Args:
            app: The main application instance.
            obj: The object that was created.
        """
        self.app = app
        self.obj = obj

    def undo(self):
        """
        Undoes the create action.
        """
        if isinstance(self.obj, self.app.HarnessComponents.Connector):
            if self.obj in self.app.HDF.connectors:
                self.app.HDF.connectors.remove(self.obj)
        elif isinstance(self.obj, self.app.HarnessComponents.Wire):
            if self.obj in self.app.HDF.wires:
                self.app.HDF.wires.remove(self.obj)

    def redo(self):
        """
        Redoes the create action.
        """
        if isinstance(self.obj, self.app.HarnessComponents.Connector):
            if self.obj not in self.app.HDF.connectors:
                self.app.HDF.connectors.append(self.obj)
        elif isinstance(self.obj, self.app.HarnessComponents.Wire):
            if self.obj not in self.app.HDF.wires:
                self.app.HDF.wires.append(self.obj)


class DeleteAction:
    """
    An action that represents deleting an object.
    """
    def __init__(self, app, obj):
        """
        Initializes a DeleteAction.

        Args:
            app: The main application instance.
            obj: The object that was deleted.
        """
        self.app = app
        self.obj = obj

    def undo(self):
        """
        Undoes the delete action.
        """
        if isinstance(self.obj, self.app.HarnessComponents.Connector):
            if self.obj not in self.app.HDF.connectors:
                self.app.HDF.connectors.append(self.obj)
        elif isinstance(self.obj, self.app.HarnessComponents.Wire):
            if self.obj not in self.app.HDF.wires:
                self.app.HDF.wires.append(self.obj)

    def redo(self):
        """
        Redoes the delete action.
        """
        if isinstance(self.obj, self.app.HarnessComponents.Connector):
            if self.obj in self.app.HDF.connectors:
                self.app.HDF.connectors.remove(self.obj)
        elif isinstance(self.obj, self.app.HarnessComponents.Wire):
            if self.obj in self.app.HDF.wires:
                self.app.HDF.wires.remove(self.obj)


class FlipAction:
    """
    An action that represents flipping an object.
    """
    def __init__(self, obj):
        """
        Initializes a FlipAction.

        Args:
            obj: The object that was flipped.
        """
        self.obj = obj

    def undo(self):
        """
        Undoes the flip action.
        """
        self.obj.flip()

    def redo(self):
        """
        Redoes the flip action.
        """
        self.obj.flip()

class CopyAction:
    """
    An action that represents copying an object.
    """
    def __init__(self, app):
        """
        Initializes a CopyAction.

        Args:
            app: The main application instance.
        """
        self.app = app
        self.clipboard_data = None

    def execute(self):
        """
        Executes the copy action.
        """
        self.clipboard_data = self.app.copy_selection()

    def undo(self):
        """
        Copy actions don't have an undo.
        """
        pass

    def redo(self):
        """
        Copy actions don't have a redo.
        """
        pass

class PasteAction:
    """
    An action that represents pasting an object.
    """
    def __init__(self, app, pasted_objects):
        """
        Initializes a PasteAction.

        Args:
            app: The main application instance.
            pasted_objects: The objects that were pasted.
        """
        self.app = app
        self.pasted_objects = pasted_objects

    def undo(self):
        """
        Undoes the paste action.
        """
        for obj in self.pasted_objects:
            if isinstance(obj, self.app.HarnessComponents.Connector):
                if obj in self.app.HDF.connectors:
                    self.app.HDF.connectors.remove(obj)
            elif isinstance(obj, self.app.HarnessComponents.Wire):
                if obj in self.app.HDF.wires:
                    self.app.HDF.wires.remove(obj)

    def redo(self):
        """
        Redoes the paste action.
        """
        for obj in self.pasted_objects:
            if isinstance(obj, self.app.HarnessComponents.Connector):
                if obj not in self.app.HDF.connectors:
                    self.app.HDF.connectors.append(obj)
            elif isinstance(obj, self.app.HarnessComponents.Wire):
                if obj not in self.app.HDF.wires:
                    self.app.HDF.wires.append(obj)
