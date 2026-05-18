"""Modul to resize a image.

This modul take a image file and resize it to 512x512 px.
"""
from PIL import Image

img = Image.open('Media_Doc/asset_1.png')

def resize_image(img):
    """Function to resize image by using LANCZOS algorythm."""
    img_resize = img.resize((512, 512), Image.Resampling.LANCZOS)
    img_resize.save('Media_Doc/asset_1_resize.png')
    return img_resize

resize_image(img)