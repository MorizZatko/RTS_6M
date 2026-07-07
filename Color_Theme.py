"""Color Theme.

This module reads a JPG file, quantizes the image to reduce the color complexity,
and sends the top 5 dominant colors to "The Color API" to retrieve their names.

--- Day 2/5 ---
"""

import cv2
import numpy as np
import requests

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

color_names = []
color_info_list = []

print("Analizing image...")
# Load image, downscale it and convert color space to RGB
org_img = cv2.imread(r"E:\Kamera\2025\JP_ZecheZollverein\Neuer Ordner\JPZoll_JPG-156.JPG")
img_resize = cv2.resize(org_img, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
rgb_img = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

# Quantize color values to group similar colors
factor = 32
quantized_img = (rgb_img // factor) * factor
flat_quantized_img = quantized_img.reshape(-1, 3)

# Find unique colors and their counts
col_val, count = np.unique(flat_quantized_img, axis=0, return_counts=True)

# Sort colors
indicies = np.argsort(count)
color_array = indicies[::-1]
actual_colors = col_val[color_array]

check_count = 0

# Reuqest names for the top 5 most dominant colors
for color in actual_colors[:5]:
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