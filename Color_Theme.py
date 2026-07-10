"""Color Theme.

This module reads a image file, detects the top 5 dominant colors and sends it to "The Color API" to retrieve their names.
After creating a expanding the canvas, it adds the colors as blocks on the right side of the image and writes their names on the blocks.
Finally, it saves the new canvas to the same dictionary with "ColorTheme" added to the file name.

--- Day 5/5 ---
"""

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading
import os

# Global variables
global_canvas = None
global_path = None
global_img = None

# Global colors
BG_COLOR = "#2b2b2b"
FG_COLOR = "#dcdcdc"

def browse_folder():
    """Opens the file dialog to browse for an image file.
    
    Returns:
        folder_selected (str): The selected file path.
    """
    folder_selected = filedialog.askopenfilename()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)
        return folder_selected
    return None


def process_image(path_entry):
    """Analyze image to detect the 5 most dominant colors via K-Means.

    Creates a new canvas with the 5 color blocks added to the image on the right side.
    Finally prints every color name onto each block.
    
    Args:
        path_entry (tk.Entry): Tkinter entry widget containing the image path.

    Returns:
        canvas_bgr (np.ndarray): Final canvas in BGR color space.
        img_path (str): The path to the processed image.
        org_img (np.ndarray): Original loaded image in BGR.
    """
    # Initialize empty lists
    color_names = []
    color_info_list = []
    
    log("Analizing image...")

    # Load image, downscale it and convert color space to RGB
    img_path = path_entry.get()
    org_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if org_img is None:
            messagebox.showerror("Error!", "Loading image failed, check path...")
            return
    
    # Convert BGR to RGB for PIL and K-Means processing
    rgb_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB)

    # Detect the 5 most dominant colors
    data = np.float32(rgb_img.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    kmeans_results = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Extract dominant colors 
    dominant_colors = None
    for res in kmeans_results:
        if isinstance(res, np.ndarray) and res.shape == (k, 3):
            dominant_colors = np.uint8(res)
            break

    if dominant_colors is None:
        log(f"K-Means didnt find color centers, check input file!")

    
    check_count = 0

    # Reuqest names for the top 5 most dominant colors
    for c in dominant_colors[:5]:
        check_count += 1
        print(f"Analyzing color {check_count}")
    
        # Prevent duplicate names in the final list
        name = get_color_name(c, check_count)
        if name not in color_names:
            color_names.append(name)
            color_info_list.append({"name": name, "rgb": c.tolist()})
        if len(color_info_list) == 5:
            break

    log(color_info_list)

    # Get original image size
    img_size = rgb_img.shape
    img_width = img_size[1]
    img_height = img_size[0]

    # Calculate dynamic width for the side panel
    min_bar_width = 300
    bar_percent = 0.2
    bar_width = max(int(img_width * bar_percent), min_bar_width)

    # Initialize empty canvas
    canvas = np.zeros((img_height, img_width + bar_width, 3), dtype=np.uint8)

    # Calculate coordinates to place the image onto the canvas
    h_start = (canvas.shape[0] - rgb_img.shape[0]) // 2
    h_end = h_start + rgb_img.shape[0]

    # Place image onto canvas
    canvas[h_start:h_end, 0:rgb_img.shape[1]] = rgb_img

    # Calculate size of color blocks
    col_bar_height = img_height // 5
    padding = int(bar_width * 0.05)

    # Convert to PIUL Image
    pil_img = Image.fromarray(canvas)
    draw = ImageDraw.Draw(pil_img)

    # Create color blocks and places their names onto them
    for index, item in enumerate(color_info_list):

        # Calculate coordinate for each color block
        y_start = index * col_bar_height
        y_end = y_start + col_bar_height
        draw.rectangle([img_width, y_start, img_width + bar_width, y_end], fill=tuple(item["rgb"]))

        # Calculate text color for good contrast
        r, g, b = item["rgb"]
        brightness = (0.299 * r) + (0.587 * g) + (0.144 * b)
        text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)

        # Dynamic font size
        dynamic_font_size = int(img_height * 0.03)
        dynamic_font_size = min(dynamic_font_size, int(bar_width * 0.1))

        # Draw text onto each color block
        text = item["name"]
        font = ImageFont.truetype("arial.ttf", dynamic_font_size)
        max_text_width = bar_width - (2 * padding)
        while font.getbbox(text)[2] > max_text_width and dynamic_font_size > 10:
            dynamic_font_size -= 2
            font = ImageFont.truetype("arial.ttf", dynamic_font_size)
        position = (img_width + padding, y_end - padding - dynamic_font_size)
        draw.text(position, text, font=font, fill=text_color)

    # Convert back to canvas
    canvas = np.array(pil_img)

    # Convert color space to BGR
    canvas_bgr = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)

    # Update global variables
    global global_canvas, global_path, global_img
    global_canvas = canvas_bgr
    global_path = img_path
    global_img = org_img

    return canvas_bgr, img_path, org_img


def show_image_gui(cv_img):
    """Displays the image in the GUI.
    
    Args:
        cv_img (np.ndarray): Original image as tuple.
    """
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img.thumbnail((1200, 800))
    img_tk = ImageTk.PhotoImage(image=pil_img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def get_color_name(color, index):
    """Fetches the color name from the API for a given RGB value.

    Args:
        color (array-like): A list or array containing [R, G, B] values.
        index (int): A fallback index used to generate a name if the request fails

    Returns:
        str: The name of the color from the API, or a fallback string.
    """
    try:
        base_url = "https://www.thecolorapi.com/id"

        # Convert color values to integers and string
        rgb_string = ",".join(map(lambda x: str(int(x)), color))
        response = requests.get(base_url, params={"rgb": rgb_string})
        if response.status_code == 200:
            log("API checked the color")
            return response.json()["name"]["value"]
        return f"Color {index}"
    except:
        messagebox.showerror("Error!", "API connection failed...")
        log(f"Error! {response.status_code}")
        return f"Color {index}"
    

def save_image(canvas_bgr, img_path):
    """Save final processed image to dictionary path with modified file name.
    
    Args:
        canvas_bgr (array): Final canvas as array.
        img_path (str): Image directory as string.
    """
    if canvas_bgr is None or img_path is None:
        messagebox.showwarning("Warning!", "Please select a image to analyze...")
        return
    name, ext = os.path.splitext(img_path)
    new_path = f"{name}_ColorTheme{ext}"
    img_save = cv2.imwrite(new_path, canvas_bgr)
    if img_save:
        messagebox.showinfo("Success!", "Image saved")
    else:
        messagebox.showerror("Error!", "Save failed")


def handle_browse():
    """Handles browse function with extra letters and messagebox."""
    path = browse_folder()
    if path:
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            messagebox.showerror("Error!", "Loading image failed, check path...")
            return
        show_image_gui(img)


def handle_analyze():
    """Disables the interface button and starts image processing in a separate thread."""
    ana_btn.config(state="disabled")
    log("Starting analysis... please wait.")
    threading.Thread(target=run_analysis_async, daemon=True).start()

def run_analysis_async():
    """Runs the processing in the background thread."""
    result = process_image(path_entry)
    root.after(0, lambda: finalize_analysis(result))

def finalize_analysis(result):
    """Updates the GUI with the processing results from the main thread.

    Args:
        result (tuple/None): The return values from process_image or None if failed.
    """
    show_image_gui(result[0])
    log("Analysis complete!")
    ana_btn.config(state="normal")

# Initialize main window
root = tk.Tk()
root.title("Color Theme Generator")
root.state('zoomed')
root.configure(bg=BG_COLOR)

# Setting left control area
ctrl_frame = tk.Frame(root, width=300, bg=BG_COLOR)
ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
log_box = tk.Text(ctrl_frame, height=120, width=40, state="disabled", bg="#1e1e1e", fg="#dcdcdc", font=("Consolas", 9))
log_box.grid(row=4, column=0, columnspan=2, pady=20)

def log(message):
    """Appends messages and a structured list of colors to the Tkinter Text log box.

    Args:
        message (str or list): The string message or color info list to display.
    """
    log_box.config(state="normal")
    if isinstance(message, list):
        for i, item in enumerate(message, 1):
            name = item.get("name", "Unknown")
            log_box.insert (tk.END, f"Color {i}: {name}\n")
    else:
        log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")

# Setting right view area
view_frame = tk.Frame(root, bg=BG_COLOR)
view_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Initialize image label
img_label = tk.Label(view_frame, bg=BG_COLOR)
img_label.pack(expand=True, fill=tk.BOTH)

# Entry field for the image dictionary
tk.Label(ctrl_frame, text="Dictionary:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=10)
path_entry = tk.Entry(ctrl_frame, width=30)
path_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

# Browse button to search a dictionary
brw_btn = tk.Button(ctrl_frame, text="Browse", command=handle_browse)
brw_btn.grid(row=1, column=0,  columnspan=2, sticky="ew")

# Button to start analyzing process
ana_btn = tk.Button(ctrl_frame, text="Analyze Image", command=handle_analyze)
ana_btn.grid(row=2, column=0,  columnspan=2, sticky="ew")

# Save button to write the final image to the dictionary
save_btn = tk.Button(ctrl_frame, text="Save Image", command=lambda: save_image(global_canvas, global_path))
save_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

root.mainloop()