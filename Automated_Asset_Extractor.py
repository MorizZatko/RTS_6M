"""Automated Asset Extractor.

This module loads an ID-Map, resizes it, and converts it to the HSV color space.
It generates a binary mask to isolate neon green areas,
and refines it using morphological closing with a 5x5 pixel kernel.

For every detected area larger than the threshold it extracts the color crop,
and the matching edge map, by using Gaussain-Blur and Canny edge detection.
Finally, every asset gets exported as color image and edge map in PNG format, 
using increasing counter in the filename.
"""

import cv2
import numpy as np

# Load image annd downscale it for better display fit
img = cv2.imread('Media_Doc/ID_Map_1.PNG')
img_resize = cv2.resize(img, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)

export_count = 0

# Color threshold mask for neon green
lower_green = np.array([50, 75, 75])
upper_green = np.array([75, 255, 255])
mask = cv2.inRange(img_hsv, lower_green, upper_green)

# Clean mask with morphological closing
kernel = np.ones((5,5), np.uint8)
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

img_display = img_hsv.copy()

# Find contours on copied mask
copy_mask = mask_clean.copy()
contours, hierarchy = cv2.findContours(copy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_display, contours, -1, (0, 255, 0,), 2)

for i, cnt in enumerate(contours):
    # Noise filter by threshold
    if cv2.contourArea(cnt) > 100:
        # Bounding box calculation and draw it on resized image
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_resize, (x, y), (x + w, y + h), (255, 0 ,0), 2)
        # Crop detected asset from the color image
        crop_color = img_resize[y:y+h, x:x+w]
        # Generates the edge map
        gray_crop = cv2.cvtColor(crop_color, cv2.COLOR_BGR2GRAY)
        blur_crop = cv2.GaussianBlur(gray_crop, (3,3), 0)
        edge_crop = cv2.Canny(blur_crop, 50, 150)

        export_count += 1
        # Saves the results
        cv2.imwrite(f'Media_Doc/Crops/asset_{export_count}_color.PNG', crop_color)
        cv2.imwrite(f'Media_Doc/Crops/asset_{export_count}_edge.PNG', edge_crop)

# Displays the final results
cv2.imshow("Orginal", img_resize)
cv2.imshow("Mask", mask)
cv2.imshow("Clean Mask", mask_clean)
cv2.waitKey(0)
cv2.destroyAllWindows()