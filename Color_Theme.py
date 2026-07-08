"""Color Theme.

This module reads a JPG file, detects the top 5 dominant colors and sends it to "The Color API" to retrieve their names.
After creating a new canvas, it adds the colors as blocks on the right side of the image and writes their names on the blocks.

--- Day 3/5 ---
"""

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont


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

# Initialize lists
color_names = []
color_info_list = []

print("Analizing image...")

# Load image, downscale it and convert color space to RGB
org_img = cv2.imread(r"E:\Kamera\2025\JP_ZecheZollverein\Neuer Ordner\JPZoll_JPG-156.JPG")
img_resize = cv2.resize(org_img, dsize=None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
rgb_img = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

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
bar_percent = 0.2
bar_width = int(img_width * bar_percent)

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
text_percent = 0.1
text_width = int(bar_width * text_percent)

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

    # Draw text onto each color block
    pil_img = Image.fromarray(canvas)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype("arial.ttf", 20)
    text = color["name"]
    position = ((img_width + text_width), (y_end - col_bar_height // 4))
    draw.text(position, text, font=font, fill=text_color)

    # Convert back to canvas
    canvas = np.array(pil_img)

# Convert color space to BGR
canvas_bgr = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)

# Show final output
cv2.imshow("Test", canvas_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()