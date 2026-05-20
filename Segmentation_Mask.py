"""Segmentation Mask.

This module converts a image to L-mode (greyscale) and converts all pixels using a threshold of 128.
All pixels greater than 128 are set to 255, while pixels less than or equal to 128 are set to 0.
"""

from PIL import Image, ImageOps

img = Image.open('Media_Doc/_MOZ4903.JPG')
img = ImageOps.exif_transpose(img)

def binary(img):
    """Converts and binarizes image."""
    img_L = img.convert('L')
    binary_img = img_L.point(lambda p: 255 if p > 128 else 0)
    binary_img.save('Media_Doc/_MOZ4903_Binary.PNG')
    binary_img.show()

binary(img)