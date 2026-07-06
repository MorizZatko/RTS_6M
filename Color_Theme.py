"""Color Theme.

This module reads a JPG file and detects the five main colors.
--- Day 1/5 ---
"""

import cv2
import numpy as np

# Load image and convert color space to RGB
org_img = cv2.imread(r"E:\Kamera\2025\JP_ZecheZollverein\Neuer Ordner\JPZoll_JPG-156.JPG")
rgb_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB)

# Reshape to 2D-Array
col_img = rgb_img.reshape(-1, 3)

# Detect and count color values
col_val, count = np.unique(col_img, axis=0, return_counts=True)

# Extract top 5 colors
indices = np.argsort(count)
top_indices = indices[-5:][::-1]
top_colors = col_val[top_indices]

# Final output
print(top_colors)