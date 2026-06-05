"""Texture Atlas.

This module loads image files from a directory, 
resize it to 256x256 pixels, and arrange them into an optimal grid layout.
It saves the texture coordinates to a JSON metadata file and displays the resulting atlas image.
"""

import cv2
import numpy as np
import os
import math
import json

assets = []
folder_path = 'Media_Doc/Textures/'
files = os.listdir(folder_path)

# Load an preprocess all valid images from the directory
for filename in files:
    full_path = os.path.join(folder_path, filename)
    img = cv2.imread(full_path)

    if img is not None:
        img_resize = cv2.resize(img, (256, 256))
        assets.append((filename, img_resize))

img_count = len(assets)

# Safe guard to stop execution if no images were loaded
if img_count == 0:
    print("Fehler! Keine gültigen Bild Daten gefunden.")

# Calculate optimal grid dimensions
num_col = math.ceil(math.sqrt(img_count))
num_row = math.ceil(img_count / num_col)

# Create blank black canvas for the atlas
atlas = np.zeros((num_row * 256, num_col * 256, 3), dtype=np.uint8)

metadata = {}

# Paste every image into its grid position
for index, (name, asset) in enumerate(assets):
    current_row = index // num_col
    current_col = index % num_col

    atlas[current_row*256 : (current_row+1)*256, current_col*256 : (current_col+1)*256] = asset

    metadata[name] = {"x": current_col * 256, "y": current_row * 256, "w": 256, "h": 256}

# Export coordinates to a JSON file
try:
    json_path = 'atlas_metadata.json'
    with open('atlas_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Erfolg! Metadaten wurden gespeichert unter: {os.path.abspath(json_path)}")
except Exception as e:
    print(f"Fehler beim speichern der JSON: {e}")

# Display final atlas image
cv2.imshow("Atlas", atlas)

# Cleanup window by press key
cv2.waitKey(0)
cv2.destroyAllWindows()