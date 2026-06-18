"""Training Set Generator.

This module loads all PNG files located in a hardcoded directory.
For every detected file it calculates the center to cut out the center square.
Finally it get resized to 512x512 pixels, set to float32 and stored as array in a 
Numpy file.
"""

import cv2
import os
import numpy as np

# Directory path with all images
dir_path = r"C:\Users\moriz\Desktop\RTS\python_start\Media_Doc"

# Get all PNG files from the directory
img_files = [f for f in os.listdir(dir_path) if f.endswith(".png")]

# Target resolution for the final images
target_size = (512, 512)

# List to store the processed image arrays
data_list = []

# Process each image file
for index, file in enumerate(img_files):
    file_path = os.path.join(dir_path, file)
    img = cv2.imread(file_path)

    if img is not None:

        # Get dimensions and detect the shorter edge
        height, width = img.shape[:2]
        min_edge = min(height, width)

        # Calculates the center square
        start_x = (width - min_edge) // 2

        # Calculating starting coordinates for the center crop
        start_y = (height - min_edge) // 2

        # Crop via Numpy slicing
        square_cut = img[start_y : start_y + min_edge, start_x : start_x + min_edge]

        # Resize the square image to float32 and normalize range
        scaled = cv2.resize(square_cut, target_size, interpolation=cv2.INTER_AREA)
        normalized = scaled.astype(np.float32) / 255.0
        data_list.append(normalized)

# Stack images to a single Numpy array and save it
dataset = np.stack(data_list)
np.save("dataset.npy", dataset)

# Print final array shape to verify dimensions
print(f"{dataset.shape}")