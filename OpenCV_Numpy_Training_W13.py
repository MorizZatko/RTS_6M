"""OpenCV Numpy Training.

This module loads a simple texture image as PNG file.
Using several separate functions, it enhance the contrast and brightness,
creates an inverted version as well as a binary mask, and places a black box
in the left corner. By using the binary mask as input it draws bounding boxes
around every detected area.
Finally, every result is displayed until a key is pressed.
"""

import cv2
import numpy as np

# Load image
img = cv2.imread(r"C:\DCC_AI_Assets\Seamless_texture_of_\diffuse_Diff_00008_.png")

contrast = 2
brightness = 1

x = 664
y = 664
w = 420
h = 420

# Color threshold for the binary mask
lower_color = np.array([0, 20, 0])
upper_color = np.array([50, 175, 255])

def adjust_image(img, brightness, contrast):
    """Handles brightness and contrast enhancement."""
    img_fl32 = img.astype(np.float32)
    img_cont = np.multiply(img_fl32, contrast)
    img_bright = np.add(img_cont, brightness)
    img_clip = np.clip(img_bright, 0, 255) 
    img_uint8 = img_clip.astype(np.uint8)
    return img_uint8

def invert_image(img):
    """Invert image."""
    inv_img = 255 - img
    return inv_img

def apply_black_box(img, x, y, w, h):
    """Place black box onto the image."""
    img_b = img
    img_b[y : y+h, x : x+w] = [0, 0, 0]
    return img_b

def create_color_mask(img, lower_color, upper_color):
    """Create color mask by threshold."""
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_iso = cv2.inRange(img_hsv, lower_color, upper_color)
    return img_iso

img_isol = create_color_mask(img, lower_color, upper_color)

mask = img_isol
original_img = img

def analyze_objects(mask, original_img):
    """Create bounding boxes for every detected area."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(original_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(original_img, (cx, cy), 5, (0, 0, 255), -1)
    return original_img

    
# Call functions
result = adjust_image(img, 50, 1.2)
inv_result = invert_image(result)
img_black = apply_black_box(img, x, y, w, h)
mark_result = analyze_objects(mask, original_img)

# Display every result
cv2.imshow("Mark", mark_result)
cv2.imshow("ISO", img_isol)
cv2.imshow("Box", img_black)
cv2.imshow("INV", inv_result)
cv2.imshow("Result", result)
cv2.waitKey(0)