"""ML Dataset Validator and Renamer.

This module creates a window where the user can browse a directory via the os explorer.
The user can enter a new file name via a entry field and choose a file format from a dropdown menu.
All found files in the directory with the choosen file format get displayed in a listbox.
By pressing "confirm", it renames every file to the entered new file name.
"""


import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def browse_folder():
    """Browse a directory and list all files matching the chosen file format."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

    all_files = os.listdir(folder_selected)
    item_count = 0
    type = cat_var.get()
    all_items.delete(0, tk.END)

    for file in all_files:
        if file.endswith(type):
            item_count += 1
            all_items.insert(item_count, file)
    
    cat = cat_var.get()
    path = path_entry.get()
    if not path:
            messagebox.showerror("Error", "Please enter path")
    elif not os.path.exists(path):
        messagebox.showerror("Error", "Path not found!")
    else:
        messagebox.showinfo(f"Success", f"Path exists! Reading [{cat}]...")

def rename_files():
    """Rename listed files using the new base name and a counter."""
    files = all_items.get(0, tk.END)
    base_name = name_entry.get()
    path = path_entry.get()
    type = cat_var.get()

    for i, filename in enumerate(files, start=1):
          old_path = os.path.join(path, f"{filename}")
          new_path = os.path.join(path, f"{base_name}_{i}.{type}")
          os.rename(old_path, new_path)

    messagebox.showinfo("Success", f"{len(files)} Assets successfully renamed")
    

# Initialize the main window
root = tk.Tk()
root.title("Asset Path Configurator")

# Setup default category value
cat_var = tk.StringVar(value="JPG")

# Label for the dictionary entry field
tk.Label(root, text="Dictionary:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
path_entry = tk.Entry(root)
path_entry.grid(row=0, column=1, padx=10, pady=10)

# Label for new file name entry field
tk.Label(root, text="New Name:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=10)

# Configure the dropdown menu to choose category
menu = tk.OptionMenu(root, cat_var, "JPG", "PNG", "TIFF")
menu.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

# Initialize listbox for all found items
all_items = tk.Listbox(root)
all_items.grid(row=2, column=0, columnspan=4, sticky="ew")

# Initialize the confirm button, which triggers the print_setting function
conf_btn = tk.Button(root, text="Rename", command=rename_files)
conf_btn.grid(row=5, column=0, columnspan=2, sticky="ew")

# Configure the browse button to trigger the browse_folder function
brw_btn = tk.Button(root, text="Browse", command=browse_folder)
brw_btn.grid(row=4, column=0,  columnspan=2, sticky="ew")

# Start the application event loop
root.mainloop()