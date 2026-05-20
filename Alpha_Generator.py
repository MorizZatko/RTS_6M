"""Alpha Generator.

This module masks out a centered circle of a image and exports a PNG.
"""
from PIL import Image, ImageOps, ImageDraw

img = Image.open('Media_Doc/_MOZ4903.JPG')
img = ImageOps.exif_transpose(img)

img_RGBA = img.convert('RGBA')

mask = Image.new('L', (5152, 7728), 0)
draw = ImageDraw.Draw(mask)
width, height = img_RGBA.size
size = min(img_RGBA.size)
left = (width - size) // 2
top = (height - size) // 2
right = left + size
bottom = top + size
draw.ellipse([(left, top), (right, bottom)], 255)
img_RGBA.putalpha(mask)
img_RGBA.save('Media_Doc/_MOZ4903_Masked.PNG')
img_RGBA.show()