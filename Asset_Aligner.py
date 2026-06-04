"""Asset Aligner.

This module loads an image, applies basic transformations (rotation, scaling, translation).
Extracts the largest contour from the transformed image, and applies a perspective warp to realign the detected object.
"""

import cv2
import numpy as np

def sort_points(pts):
    """Sorts coordinates into a consistent order: top-left, top-right, bottom-right, bottom-left.
    
    Args:
        pts (numpy.ndarray): Array of 4 points with shape (4, 2).
    
    Returns:
        numpy.ndarray: Sorted points array of shape (4, 2) and type float32.
    """
    # Summing the coordinates
    s =pts.sum(axis=1)
    # Calculating the difference
    diff = np.diff(pts, axis=1)

    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = pts[np.argmin(s)] # Top-left
    rect[1] = pts[np.argmin(diff)] # Top-right
    rect[2] = pts[np.argmax(s)] # Bottom-right
    rect[3] = pts[np.argmax(diff)] # Bottom-left
    return rect

# Load and resize image
img = cv2.imread('Media_Doc/ID_Map_1.PNG')
img_resize = cv2.resize(img, dsize=None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)

# Define center point and rotate by 12 degrees and scale down by 0.5
center = (img_resize.shape[1] // 2, img_resize.shape[0] // 2)
m_rotation = cv2.getRotationMatrix2D(center, 12, 0.5)
rotated = cv2.warpAffine(img_resize, m_rotation, (img_resize.shape[1], img_resize.shape[0]))

# Apply translation (shift 10px right, 5px down)
m_translation = np.float32([[1, 0, 10], [0, 1, 5]])
shifted = cv2.warpAffine(rotated, m_translation, (img_resize.shape[1], img_resize.shape[0]))

# Convert to grayscale and apply binary mask by threshold
shifted_gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
_, shifted_binary = cv2.threshold(shifted_gray, 50, 255, cv2.THRESH_BINARY)

# Find contours and select the one with the largest area
contours = cv2.findContours(shifted_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
cnt = max(contours, key=cv2.contourArea)

# Flatten contour array to a list of (x, y) coordinates
pts = cnt.reshape(-1, 2)

# Find the extreme points
top_pt = pts[np.argmin(pts[:, 1])]
bottom_pt = pts[np.argmax(pts[:, 1])]
left_pt = pts[np.argmin(pts[:, 0])]
right_pt = pts[np.argmax(pts[:, 0])]

# Combine extreme points an sort them into rectangular order
src_points = np.array([top_pt, bottom_pt, left_pt, right_pt], dtype="float32")
rect = sort_points(src_points)

# Define destination coordinates for a square 1030x1030 output
dst = np.float32([[0, 0], [1030, 0], [1030, 1030], [0, 1030]])

# Calculate the transformation matrix and warp the image
matrix = cv2.getPerspectiveTransform(rect, dst)
warped = cv2.warpPerspective(shifted, matrix, (1030, 1030))

# Show the results
cv2.imshow("Warped", warped)
cv2.imshow("Rotated", rotated)
cv2.imshow("Shifted", shifted)
cv2.imshow("Binary", shifted_binary)

# Cleanup window by key press
cv2.waitKey(0)
cv2.destroyAllWindows()