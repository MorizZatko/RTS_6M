import tkinter as tk
from tkinter import filedialog

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def print_settings():
    cat = cat_var.get()
    path = path_entry.get()
    print(f"Path: {path}, Category: {cat}")

root = tk.Tk()
root.title("Asset Path Configurator")

cat_var = tk.StringVar(value="Mesh")

tk.Label(root, text="Dictionary:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
path_entry = tk.Entry(root)
path_entry.grid(row=0, column=1, padx=10, pady=10)

menu = tk.OptionMenu(root, cat_var, "Mesh", "Texture", "Animation")
menu.grid(row=1, column=0, sticky="s", padx=10, pady=10)

conf_btn = tk.Button(root, text="Confirm", command=print_settings)
conf_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

brw_btn = tk.Button(root, text="Browse", command=browse_folder)
brw_btn.grid(row=2, column=0,  columnspan=2, sticky="ew")

root.mainloop()