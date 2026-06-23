"""Tkinter Training Task 2.

This module creates a window with three labels and entry field for each.
At the bottom is a save button with out any deeper logic.
"""

import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("Asset Manager")

# Define grid layout for Labels
tk.Label(root, text="Asset Name:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
tk.Label(root, text="Asset Type:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
tk.Label(root, text="Version:").grid(row=2, column=0, sticky="w", padx=10, pady=10)

# Define layout for Entry fields
tk.Entry(root).grid(row=0, column=1, padx=10, pady=10)
tk.Entry(root).grid(row=1, column=1, padx=10, pady=10)
tk.Entry(root).grid(row=2, column=1, padx=10, pady=10)

# Configure the save button
save_btn = tk.Button(root, text="Save")
save_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

# Start the application event loop
root.mainloop()