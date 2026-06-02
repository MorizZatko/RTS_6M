"""Outline Mask.

This module loads an ID-Map from a PNG image, converts it to HSV color space.
It isolates green areas using a color threshold mask.
Through erode modifier it generates a outline by a 3x3 pixel kernel and delitates it with a
vertical kernel by 5x5 pixels. A neon green glowing outline is then generated for each area using 
morphologic gradient operation, wich finally overlaid onto the original image.
"""
import cv2
import numpy as np

# Load source image and convert to HSV
img = cv2.imread('Media_Doc/ID_Map_1.PNG')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define color range for binary mask
lower_green = np.array([50, 75, 75])
upper_green = np.array([75, 255, 255])
mask = cv2.inRange(img_hsv, lower_green, upper_green)

# Manual outline via substraction (Erosion)
kernel = np.ones((3,3), np.uint8)
eroded = cv2.erode(mask, kernel, iterations=1)
outline = cv2.subtract(mask, eroded)

# Manual outline via substraction (Deliation with vertical kernel)
kernel_v = np.zeros((5,5), np.uint8)
kernel_v[:, 2] = 1
dilated = cv2.dilate(mask, kernel_v, iterations=1)
outer_outline = cv2.subtract(dilated, mask)

# Combine both outlines
line_combo = cv2.bitwise_or(outline, outer_outline)

# Standart morphological gradient 
gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)

# Generates the final neon green outline onto the source image
green_layer = np.full(img.shape, (0, 255, 0), dtype=np.uint8)
green_outline = cv2.bitwise_and(green_layer, green_layer, mask=gradient)
final_output = cv2.add(img, green_outline)

# Display all steps and the final result
cv2.imshow("Gradient", gradient)
cv2.imshow("Combo", line_combo)
cv2.imshow("Mask", mask)
cv2.imshow("Outer", outer_outline)
cv2.imshow("Final", final_output)

# Keep windows open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()