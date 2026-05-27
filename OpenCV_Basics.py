"""OpenCV Basics.

First touch with OpenCV, this module scans the size of an image,
calculates the center coordinates and crops a 256x256 pixel area from the middle.
Finally saves the result to the local directory.
"""

import cv2

img = cv2.imread('Media_Doc/Roughness_Map_1.PNG')

img_size = img.shape

img_width = img_size[1]
img_height = img_size[0]
y_mid = img_height // 2
x_mid = img_width // 2
y_start = y_mid - 128
y_end = y_mid + 128
x_start = x_mid - 128
x_end = x_mid + 128
crop_img = img[y_start:y_end, x_start:x_end]

img_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
cv2.imwrite("Media_doc/First_CV_Crop.PNG", img_rgb)
cv2.imshow('Test', img_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()