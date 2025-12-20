"""
This module defines the connector library window for the HarnessIT application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import csv
import os

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
        self.window.title("Connector Library")
        self.window.geometry("800x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.filtered_library = self.app.library
        self.callback = callback

        self._init_ui()
        self.load_library_table()

    def _init_ui(self):
        """Initializes the user interface components."""
        # Search UI
        search_frame = ttk.Frame(self.window)
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Label(search_frame, text="MFR:").grid(row=0, column=0, padx=5)
        self.mfr_search = ttk.Entry(search_frame)
        self.mfr_search.grid(row=0, column=1, padx=5)

        ttk.Label(search_frame, text="Part #:").grid(row=0, column=2, padx=5)
        self.part_num_search = ttk.Entry(search_frame)
        self.part_num_search.grid(row=0, column=3, padx=5)

        ttk.Label(search_frame, text="Pins:").grid(row=0, column=4, padx=5)
        self.pins_search = ttk.Entry(search_frame)
        self.pins_search.grid(row=0, column=5, padx=5)

        ttk.Label(search_frame, text="Pin Type:").grid(row=0, column=6, padx=5)
        self.pin_type_search = ttk.Entry(search_frame)
        self.pin_type_search.grid(row=0, column=7, padx=5)

        self.search_button = ttk.Button(search_frame, text="Search", command=self.filter_library)
        self.search_button.grid(row=0, column=8, padx=10)

        self.clear_button = ttk.Button(search_frame, text="Clear", command=self.clear_filter)
        self.clear_button.grid(row=0, column=9, padx=5)

        # Main frame with canvas and scrollbar
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add New Connector Button
        add_button_frame = ttk.Frame(self.window)
        add_button_frame.pack(pady=10)
        self.add_button = ttk.Button(add_button_frame, text="Add New Connector", command=self.add_new_connector)
        self.add_button.pack()

    def on_close(self):
        """
        Handles the closing of the library window.
        """
        self.app.libwin = None
        self.window.destroy()

    def filter_library(self):
        """Filters the library based on the search criteria."""
        mfr = self.mfr_search.get().lower()
        part_num = self.part_num_search.get().lower()
        pins = self.pins_search.get()
        pin_type = self.pin_type_search.get().lower()

        self.filtered_library = [
            row for row in self.app.library
            if (not mfr or mfr in row.get("MFR", "").lower()) and
               (not part_num or part_num in row.get("MFR_Part_Number", "").lower()) and
               (not pins or pins == row.get("Positions", "")) and
               (not pin_type or pin_type in row.get("PinType", "").lower())
        ]
        self.load_library_table()

    def clear_filter(self):
        """Clears the search filter and reloads the table."""
        self.mfr_search.delete(0, tk.END)
        self.part_num_search.delete(0, tk.END)
        self.pins_search.delete(0, tk.END)
        self.pin_type_search.delete(0, tk.END)
        self.filtered_library = self.app.library
        self.load_library_table()

    def load_library_table(self):
        """
        Loads the connector library table with the filtered data.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Select", "MFR", "Part Number", "Description", "Positions", "PinType"]
        for col, header in enumerate(headers):
            ttk.Label(self.scrollable_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        for row_idx, item in enumerate(self.filtered_library, start=1):
            ttk.Button(self.scrollable_frame, text="Select", command=lambda id=item["ID"]: self.app.set_current(id)).grid(row=row_idx, column=0, padx=5)
            ttk.Label(self.scrollable_frame, text=item.get("MFR", "")).grid(row=row_idx, column=1, padx=5)
            ttk.Label(self.scrollable_frame, text=item.get("MFR_Part_Number", "")).grid(row=row_idx, column=2, padx=5)
            ttk.Label(self.scrollable_frame, text=item.get("Description", "")).grid(row=row_idx, column=3, padx=5)
            ttk.Label(self.scrollable_frame, text=item.get("Positions", "")).grid(row=row_idx, column=4, padx=5)
            ttk.Label(self.scrollable_frame, text=item.get("PinType", "")).grid(row=row_idx, column=5, padx=5)

    def add_new_connector(self):
        """Opens a dialog to add a new connector."""
        dialog = AddConnectorDialog(self.window)
        self.window.wait_window(dialog.top)
        
        if dialog.new_connector_data:
            new_id = str(max([int(c["ID"]) for c in self.app.library]) + 1)
            dialog.new_connector_data["ID"] = new_id
            
            self.app.library.append(dialog.new_connector_data)
            self.save_library_to_csv()
            self.clear_filter()

    def save_library_to_csv(self):
        """Saves the library to the CSV file."""
        filepath = 'resources/library/Connectors.csv'
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.app.library[0].keys())
            writer.writeheader()
            writer.writerows(self.app.library)


class AddConnectorDialog:
    """
    A dialog for adding a new connector to the library.
    """
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Connector")
        self.new_connector_data = None

        self.fields = ["MFR", "MFR_Part_Number", "Description", "Positions", "PinType", "ImageLocation"]
        self.entries = {}

        for i, field in enumerate(self.fields):
            ttk.Label(self.top, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            if field == "ImageLocation":
                self.entries[field] = ttk.Entry(self.top, width=40)
                self.entries[field].grid(row=i, column=1, padx=10, pady=5)
                ttk.Button(self.top, text="Browse...", command=self.browse_image).grid(row=i, column=2, padx=5)
            else:
                self.entries[field] = ttk.Entry(self.top, width=40)
                self.entries[field].grid(row=i, column=1, padx=10, pady=5)

        ttk.Button(self.top, text="Save", command=self.save).grid(row=len(self.fields), column=0, columnspan=3, pady=10)

    def browse_image(self):
        """Opens a file dialog to select an image."""
        filepath = filedialog.askopenfilename(
            initialdir="resources/images",
            title="Select an Image",
            filetypes=(("PNG files", "*.png"), ("all files", "*.*"))
        )
        if filepath:
            # Make the path relative to the project root
            rel_path = os.path.relpath(filepath, os.getcwd())
            self.entries["ImageLocation"].delete(0, tk.END)
            self.entries["ImageLocation"].insert(0, rel_path.replace("\\", "/"))

    def save(self):
        """Saves the new connector data and closes the dialog."""
        self.new_connector_data = {field: self.entries[field].get() for field in self.fields}
        self.top.destroy()
