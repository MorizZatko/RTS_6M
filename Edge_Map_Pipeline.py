"""Edge Map Pipeline.

This module takes a PNG roughness map, converts it to grayscale, 
blurs it using the gaussianblur algrorithm, and detects edges using Canny thresholds.
Finally it closes gaps in the binary image with a 3x3 morphology kernel and safes the result to the local directory.
"""

import cv2
import numpy as np

img = cv2.imread('Media_Doc/Roughness_Map_1.PNG')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
img_edges = cv2.Canny(img_blur, threshold1=150, threshold2=333)

kernel = np.ones((3,3), np.uint8)
img_cleaned = cv2.morphologyEx(img_edges, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Grayscale", img_gray)
cv2.imshow("Blurred", img_blur)
cv2.imshow("Edges", img_edges)
cv2.imshow("Cleaned", img_cleaned)
cv2.imwrite('Media_Doc/Edge_Map_1.PNG', img_cleaned)
cv2.waitKey(0)
cv2.destroyAllWindows()