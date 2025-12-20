# HarnessIT

HarnessIT is a lightweight harness editor designed for creating and managing wiring harness diagrams.

## Features

- **Visual Harness Editing:** Create and manipulate harness diagrams with a graphical interface.
- **Component Library:** A library of connectors that can be extended by the user.
- **Wire and Connector Properties:** Edit properties of wires and connectors, such as name, part number, color, and gauge.
- **Cut Sheet Generation:** Automatically generate a cut sheet for the created harness.
- **Undo/Redo:** Full undo/redo support for all actions.
- **Save/Open:** Save your work and open existing harness files.
- **Zoom and Pan:** Easily navigate large harness diagrams.
- **Grid and Snapping:** A configurable grid and snapping system for precise component placement.
- **Copy/Paste:** Duplicate harness components and structures.
- **Context-Sensitive Menus:** Right-click on any object to access a context-sensitive menu with relevant actions.

## How to Use

### Adding and Manipulating Components

- **Add a Connector:**
  - Click the "Add Connector" button in the ribbon or press the `A` key.
  - Select a connector from the library.
  - Click on the canvas to place the connector.
- **Add a Wire:**
  - Click the "Add Wire" button in the ribbon or press the `W` key.
  - Click on two connector pins to create a wire between them.
- **Move an Object:**
  - Click and drag an object to move it.
  - Alternatively, select an object and use the "Move" button in the ribbon or press the `M` key to enter "move mode".
- **Select an Object:**
  - Click on an object to select it.
  - The properties of the selected object will be displayed in the sidebar.
- **Delete an Object:**
  - Select an object and press the `Delete` key.
  - Alternatively, right-click on an object and select "Delete" from the context menu.
- **Flip a Connector:**
  - Select a connector and press the `F` key.
  - Alternatively, right-click on a connector and select "Flip" from the context menu.

### Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New Harness |
| `Ctrl+O` | Open Harness |
| `Ctrl+S` | Save Harness |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select All |
| `Ctrl+L` | Open Connector Library |
| `A` | Add Connector Mode |
| `W` | Add Wire Mode |
| `S` | Select Mode |
| `M` | Move Mode |
| `F` | Flip Connector |
| `Delete` | Delete Selection |
| `Escape` | Cancel Current Mode |
| `Ctrl` + `MouseWheel` | Zoom In/Out |

### Menu Items

- **File**
  - **New:** Creates a new, empty harness.
  - **Open:** Opens an existing harness file.
  - **Save:** Saves the current harness to a file.
- **Edit**
  - **Undo:** Undoes the last action.
  - **Redo:** Redoes the last undone action.
  - **Copy:** Copies the selected objects to the clipboard.
  - **Paste:** Pastes the objects from the clipboard to the canvas.
- **Grid**
  - **Show Grid:** Toggles the visibility of the grid.
  - **Snap to Grid:** Toggles the grid snapping functionality.

## Contributing

This project is a work in progress, and contributions are welcome. If you would like to contribute, please feel free to fork the repository and submit a pull request.
