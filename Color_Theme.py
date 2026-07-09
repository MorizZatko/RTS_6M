"""Color Theme.

This module reads a JPG file, detects the top 5 dominant colors and sends it to "The Color API" to retrieve their names.
After creating a new canvas, it adds the colors as blocks on the right side of the image and writes their names on the blocks.

--- Day 3/5 ---
"""

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

global_canvas = None
global_path = None
global_img = None

def browse_folder():
    """Function to browse a directory via system explorer."""
    folder_selected = filedialog.askopenfilename()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)
        return folder_selected
    return None

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
            print("API checked the color")
            return response.json()["name"]["value"]
        else:
            return f"Color {index}"
    except:

        # Fallback if the network request fails 
        return f"Color {index}"


def process_image(path_entry):

    color_names = []
    color_info_list = []
    
    print("Analizing image...")

    # Load image, downscale it and convert color space to RGB
    img_path = path_entry.get()
    org_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if org_img is None:
            messagebox.showerror("Error!", "Loading image failed, check path...")
            return
    rgb_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB)

    # Detect the 5 most dominant colors
    data = np.float32(rgb_img.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    _, name, color = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_colors = np.uint8(color)

    # Initialize check count
    check_count = 0

    # Reuqest names for the top 5 most dominant colors
    for color in dominant_colors[:5]:
        check_count += 1
        print(f"Analyzing color {check_count}")
    
        # Prevent duplicate names in the final list
        name = get_color_name(color, check_count)
        if name not in color_names:
            color_names.append(name)
            color_data = {
            "name": name,
            "rgb": color.tolist()
            }
            color_info_list.append(color_data)
        if len(color_info_list) == 5:
            break

    print(color_info_list)

    # Get image size
    img_size = rgb_img.shape
    img_width = img_size[1]
    img_height = img_size[0]

    # Setting color bar width
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
    canvas_size = canvas.shape
    canvas_width = canvas_size[1]

    # Calculate text width for positioning onto the block
    text_width = int(bar_width * 0.05)

    pil_img = Image.fromarray(canvas)

    # Create color blocks and places their names onto them
    for index, color in enumerate(color_info_list):

        # Calculate coordinate for each color block
        y_start = index * col_bar_height
        y_end = y_start + col_bar_height
        canvas[y_start:y_end, img_width : img_width + bar_width] = color["rgb"]

        # Calculate text color for good contrast
        r, g, b = color["rgb"]
        brightness = (0.299 * r) + (0.587 * g) + (0.144 * b)
        text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)

        # Dynamic font size
        dynamic_font_size = int(img_height * 0.03)

        # Draw text onto each color block
        
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype("arial.ttf", dynamic_font_size)
        text = color["name"]
        position = ((img_width + text_width), (y_end - col_bar_height // 4))
        draw.text(position, text, font=font, fill=text_color)

    # Convert back to canvas
    canvas = np.array(pil_img)

    # Convert color space to BGR
    canvas_bgr = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)

    global global_canvas, global_path, global_img
    global_canvas = canvas_bgr
    global_path = img_path
    global_img = org_img

    return canvas_bgr, img_path, org_img

def save_image(canvas_bgr, img_path):
    if canvas_bgr is None or img_path is None:
        messagebox.showwarning("Warning!", "Please select a image to analyze...")
        return
    img_save = cv2.imwrite(img_path, canvas_bgr)
    if img_save:
        messagebox.showinfo("Success!", "Image saved")
    else:
        messagebox.showerror("Error!", "Save failed")

def show_image_gui(cv_img):
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img.thumbnail((1200, 800))
    img_tk = ImageTk.PhotoImage(image=pil_img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

def handle_browse():
    path = browse_folder()
    if path:
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            messagebox.showerror("Error!", "Loading image failed, check path...")
            return
        show_image_gui(img)

def handle_analyze():
    result = process_image(path_entry)
    canvas_bgr = result[0]
    show_image_gui(canvas_bgr)

root = tk.Tk()
root.title("Color Theme Generator")
root.state('zoomed')

ctrl_frame = tk.Frame(root, width=300)
ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

view_frame = tk.Frame(root)
view_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

img_label = tk.Label(view_frame)
img_label.pack(expand=True, fill=tk.BOTH)

tk.Label(ctrl_frame, text="Dictionary:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
path_entry = tk.Entry(ctrl_frame)
path_entry.grid(row=0, column=1, padx=10, pady=10)

brw_btn = tk.Button(ctrl_frame, text="Browse", command=handle_browse)
brw_btn.grid(row=1, column=0,  columnspan=2, sticky="ew")

ana_btn = tk.Button(ctrl_frame, text="Analyze Image", command=handle_analyze)
ana_btn.grid(row=2, column=0,  columnspan=2, sticky="ew")

save_btn = tk.Button(ctrl_frame, text="Save Image", command=lambda: save_image(global_canvas, global_path))
save_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

root.mainloop()