"""HSV Binary Mask.

This module loads an image, resizes ot and opens a UI with trackbars
to adjust HSV ranges for isolating red colors.
"""

import cv2
import numpy as np

# Load source Image and preprocessing
img = cv2.imread('Media_Doc/fabric_pattern_1.PNG')
img_resize = cv2.resize(img, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)

# UI trackbars setup
cv2.namedWindow("Settings")
cv2.createTrackbar("Lower_Red_H", "Settings", 0, 10, lambda x: None)
cv2.createTrackbar("Upper_Red_H", "Settings", 170, 179, lambda x: None)
cv2.createTrackbar("Lower_Red_S", "Settings", 50, 128, lambda x: None)
cv2.createTrackbar("Upper_Red_S", "Settings", 128, 255, lambda x: None)
cv2.createTrackbar("Lower_Red_V", "Settings", 50, 128, lambda x: None)
cv2.createTrackbar("Upper_Red_V", "Settings", 128, 255, lambda x: None)

# Processing loop
while True:
    # Current slider positions
    Lower_Red_S_value = cv2.getTrackbarPos("Lower_Red_S", "Settings")
    Upper_Red_S_value = cv2.getTrackbarPos("Upper_Red_S", "Settings")
    Lower_Red_V_value = cv2.getTrackbarPos("Lower_Red_V", "Settings")
    Upper_Red_V_value = cv2.getTrackbarPos("Upper_Red_V", "Settings")

    # Lower red spectrum mask
    lower_red = np.array([0, Lower_Red_S_value, Lower_Red_V_value])
    upper_red = np.array([10, Upper_Red_S_value, Upper_Red_V_value])
    mask_red = cv2.inRange(img_hsv, lower_red, upper_red)

    # Upper red spectrum mask
    lower_red_2 = np.array([160, Lower_Red_S_value, Lower_Red_V_value])
    upper_red_2 = np.array([179, Upper_Red_S_value, Upper_Red_V_value])
    mask_red_2 = cv2.inRange(img_hsv, lower_red_2, upper_red_2)

    # Combine both masks to capture full red spectrum
    final_result = cv2.bitwise_or(mask_red, mask_red_2)

    # Apply final mask to source image
    color_result = cv2.bitwise_and(img_resize, img_resize, mask=final_result)

    # Display results in separate windows
    cv2.imshow("Final Mask", final_result)
    cv2.imshow("Color Mask", color_result)
    cv2.imshow("Input", img_resize)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()