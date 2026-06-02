"""Layer Mixer.

This module loads two texture images from jpeg files. If the import fails or the dimension dont match, it prints an error message.
After resizing the images for efficiency, it blends them together and calculates their difference.
Finally, it converts the difference to grayscale and applies a binary threshold of 30 to create the final output.
"""

import cv2
import numpy as np

# Load both texture images
img_1 = cv2.imread('Media_Doc/aerial_wood_snips_diff_4k.JPG')
img_2 = cv2.imread('Media_Doc/dirt_aerial_03_diff_4k.JPG')

# Validate image imports and dimensions
if img_1 is None or img_2 is None:
    print("Fehler: Eines der Bilder konnte nicht geladen werden, bitte Pfad überprüfen!")
elif img_1.shape != img_2.shape:
    print("Fehler: Bildgrößen stimmen nicht überein!")
else:
    print("Bilder wurden erfolgreich geladen!")

# Resize images to 25% of original size for faster processing
img_1_resize = cv2.resize(img_1, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
img_2_resize = cv2.resize(img_2, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

# Blend botch images with equal weight (50% each) and calculates the total difference
blended = cv2.addWeighted(img_1_resize, 0.5, img_2_resize, 0.5, 0)
diff = cv2.absdiff(img_1_resize, img_2_resize)

# Convert the difference image to grayscale and creates the final binary mask by threshold of 30
diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, diff_mask = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

# Display the results
cv2.imshow("Blend", blended)
cv2.imshow("Diff", diff)
cv2.imshow("Diff Mask", diff_mask)

# Keep windows open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()