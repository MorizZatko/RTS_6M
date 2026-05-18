"""Box cropping tool.

This module crops a image in box format, based on exif orientation.
"""

from PIL import Image, ImageOps

img = Image.open('Media_Doc/_MOZ4903.jpg')
img = ImageOps.exif_transpose(img)

def center_crop(img):
    """Function to crop image calculated by image size."""
    image_width = img.width
    image_height = img.height
    dif = image_height - image_width
    start = int(dif // 2)
    end = image_width + start
    crop_img = img.crop((0, start, image_width, end))
    crop_img.save('Media_Doc/_MOZ4903_cropped.jpg')
    crop_img.show()
    return crop_img

center_crop(img) 