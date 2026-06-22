"""TKinter Trainings Task 1.

This module is my first experience with Tkinter GUI.
It creates a window with two buttons, to start the process and reset it.
Both are only UI outputs with no deeper logic.
"""

import tkinter as tk

# Function to update label status
def update_status(new_text):
    """Variable to update label status.
    
    Args:
        new_text (string): String for label status.
    """
    status_var.set(new_text)

# Initialize window with title
root = tk.Tk()
root.title("Asset Pipeline Monitor")

# Setup string variable
status_var = tk.StringVar(value="System Status: Idle")
new_text = "Start Processing"

# Initialize the label with padding
label = tk.Label(root, textvariable=status_var)
label.pack(padx=64, pady=64)

# Setup button to start processing UI output
label_btn = tk.Button(root, text="Start", command=lambda: update_status("Processing..."))
label_btn.pack()

# Setup button to reset UI output
reset_btn = tk.Button(root, text="Reset", command=lambda: update_status("System Status: Idle"))
reset_btn.pack()

root.mainloop()