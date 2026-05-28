"""Object_Extraction_Pipeline.

This module processes a fabric pattern texture to isolate red colors,
by using dynamicx HSV thresholding. To get every red-like color its combining
two masks, due to the red location on the HSV color space.

UI trackbars allows the user to fine-tune the saturation and value limits.
By pressing 's' key, the module detects contours within the mask, draws bounding boxes
and crops/saves every cropped element to the directory.
"""

import cv2
import numpy as np

# Image import and preprocessing
img = cv2.imread('Media_Doc/fabric_pattern_1.PNG')
img_resize = cv2.resize(img, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)

# UI trackbar setup
cv2.namedWindow("Settings")
cv2.createTrackbar("Lower_Red_H", "Settings", 0, 10, lambda x: None)
cv2.createTrackbar("Upper_Red_H", "Settings", 170, 179, lambda x: None)
cv2.createTrackbar("Lower_Red_S", "Settings", 50, 128, lambda x: None)
cv2.createTrackbar("Upper_Red_S", "Settings", 128, 255, lambda x: None)
cv2.createTrackbar("Lower_Red_V", "Settings", 50, 128, lambda x: None)
cv2.createTrackbar("Upper_Red_V", "Settings", 128, 255, lambda x: None)
save_count = 0

# Processing Loop
while True:
    dislpay_img = img_resize.copy()

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

    # Contour extraction and visualization
    copy_mask = final_result.copy()
    contours, hierarchy = cv2.findContours(copy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(dislpay_img, contours, -1, (0, 255, 0,), 2)

    key = cv2.waitKey(1) & 0xFF

    # Segmentation and export automation
    if key == ord('s'):
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img_resize, (x, y), (x + w, y + h), (255, 0 ,0), 2)
                crop = dislpay_img[y : y+h, x : x+w]
                save_count += 1
                cv2.imwrite(f"Media_Doc/Crops/crop_{save_count}.PNG", crop)
        pass

    cv2.imshow("Final Mask", final_result)
    cv2.imshow("Color Mask", color_result)
    cv2.imshow("Input", dislpay_img)
    
    if key == ord('q'):
        cv2.destroyAllWindows()
        break