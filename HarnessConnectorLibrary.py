"""
This module defines the connector library window for the HarnessIT application.
"""

import tkinter as tk
import tkinter.ttk as ttk
import csv


class ConnectorLibrary():
    """
    The connector library window for the HarnessIT application.
    """
    def __init__(self,parent,app, callback=None):
        """
        Initializes the ConnectorLibrary.

        Args:
            parent: The parent widget.
            app: The main application instance.
            callback (function, optional): A callback function to be called when a connector is selected. Defaults to None.
        """
        self.app = app
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.geometry("600x300")
        self.Datatable = {}
        self.scrollbar = tk.Scrollbar(self.window, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # grid(column=1,row = 0)
        self.frame = tk.Canvas(self.window, scrollregion=(0,0,1000,5000),width=600, height=400)
        self.load_library_table()
        self.scrollbar.config(command=self.scroll)
        self.frame.pack(side=tk.LEFT,fill=tk.BOTH)#grid(column=0, row=0)
        self.top = 0
        self.callback = callback


    def printargs(self,*args):
        """
        Prints the given arguments to the console.
        """
        for i in args:
            print(i)
    def scroll(self,cm = 0,amount=0,units=0):
        """
        Scrolls the library table.
        """
        if cm == "scroll":
            if self.top <= 0:
                self.top -= int(amount)
                if self.top > 0:
                    self.top = 0
                self.load_library_table(self.top)
        if cm == "moveto":
            self.top = 0 - int(round(float(amount) * 100) / 2)
            if self.top > 0:
                self.top = 0
            self.load_library_table(self.top)
        normalized_scoll_pos =(self.top ) * -1 / len(self.app.library)
        print(normalized_scoll_pos)
        if normalized_scoll_pos > 1:
            self.top = len(self.app.library)
            normalized_scoll_pos = 1
        if normalized_scoll_pos < 0:
            self.top = 0
            normalized_scoll_pos = 0
        self.scrollbar.set(normalized_scoll_pos,normalized_scoll_pos +.01)
    def load_library_table(self, rw = 0):
        """
        Loads the connector library table.
        """
        r = rw
        #c = 0
        for i in self.app.library:
            if r >= 0:
                button = ttk.Button(self.frame, text= "select", command= lambda id = i["ID"]: self.app.set_current(id))
                button.grid(column=0,row =r)

                MFREntry = tk.Entry(self.frame,width=12)
                MFREntry.insert(0,i["MFR"])
                MFREntry.grid(column=1,row=r)
                MFRPNEntry = tk.Entry(self.frame,width = 12)
                MFRPNEntry.insert(0,i["MFR_Part_Number"])
                MFRPNEntry.grid(column=2,row=r)
                descEntry = tk.Entry(self.frame, width= 30)
                descEntry.insert(0,i["Description"])
                descEntry.grid(column=3,row=r)
            r += 1
