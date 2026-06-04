"""Image Pyramids.

This module loads an texture map as a JPG file and downsamples it by applying three Gaussain pyramid modifiers.
The smallest Gaussain version is then upscaled three times. Finally, a Laplacian detail map is calculated,
by taken the difference between the original and the rescaled image.
"""

import cv2
import numpy as np

# Load and resize the texture map
img = cv2.imread('Media_Doc/marble_cliff_06_diff_4k.JPG')
img_resize = cv2.resize(img, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

# Downsample: 3 Layers of Gaussain pyramid
down_1 = cv2.pyrDown(img_resize)
down_2 = cv2.pyrDown(down_1)
down_3 = cv2.pyrDown(down_2)

# Upscale: 3 Layers of Laplacian pyramid
up_1 = cv2.pyrUp(down_3)
up_2 = cv2.pyrUp(up_1)
up_3 = cv2.pyrUp(up_2)

# Calculate and enhance the detail map by finding the difference
diff = cv2.absdiff(img_resize, up_3)
detail_map = np.clip(diff.astype(np.int16) * 10, 0, 255).astype(np.uint8)

# Display results
cv2.imshow("Resized Original", img_resize)
cv2.imshow("Down 3", down_3)
cv2.imshow("Up 3", up_3)
cv2.imshow("Laplace", detail_map)

# Cleanup windows by key press
cv2.waitKey(0)
cv2.destroyAllWindows()