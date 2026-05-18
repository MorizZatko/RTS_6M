"""Modul to resize a image.

This modul take a image file and resize it to 512x512 px.
"""
from PIL import Image

img = Image.open('Media_Doc/asset_1.png')
img_resize = img.resize((512, 512), resample=Image.LANCZOS)
img_resize.save('Media_Doc/asset_1_resize.png')
img_resize.show()