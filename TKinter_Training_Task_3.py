"""TKinter Training Task 3.

This module initializes a small window with a labeled path entry field,
as well as a dropdown menu to select a category. The module checks if
the entry field is empty, verifies whether the entered path exists, and outputs 
a specific info or error message via TKinters messagebox feature.
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


def browse_folder():
    """Function to browse a directory via system explorer."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def print_settings():
    """Function to print and proof user input."""
    cat = cat_var.get()
    path = path_entry.get()
    if not path:
            messagebox.showerror("Error", "Please enter path")
    elif not os.path.exists(path):
        messagebox.showerror("Error", "Path not found!")
    else:
        messagebox.showinfo(f"Success", f"Path exists! Processing [{cat}]...")

    print(f"Path: {path}, Category: {cat}")

# Initialize the main window
root = tk.Tk()
root.title("Asset Path Configurator")

# Setup default category value
cat_var = tk.StringVar(value="Mesh")

# Label for the dictionary entry field
tk.Label(root, text="Dictionary:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
path_entry = tk.Entry(root)
path_entry.grid(row=0, column=1, padx=10, pady=10)

# Configure the dropdown menu to choose category
menu = tk.OptionMenu(root, cat_var, "Mesh", "Texture", "Animation")
menu.grid(row=1, column=0, sticky="s", padx=10, pady=10)

# Initialize the confirm button, which triggers the print_setting function
conf_btn = tk.Button(root, text="Confirm", command=print_settings)
conf_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

# Configure the browse button to trigger the browse_folder function
brw_btn = tk.Button(root, text="Browse", command=browse_folder)
brw_btn.grid(row=2, column=0,  columnspan=2, sticky="ew")

# Start the application event loop
root.mainloop()