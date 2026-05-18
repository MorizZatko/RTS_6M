"""PNG to JPEG(RGB) converter.

This modul convert a PNG-Picture to a JPEG-Picture and transfer to RGB color channel.
"""

from PIL import Image

img = Image.open('Media_Doc/asset_1.png')
img_convert = img.convert('RGB')
img_convert.save('Media_Doc/asset_1_RGB.jpeg')
img_convert.show()