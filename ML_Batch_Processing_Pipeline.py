"""ML Batch Processor Pipeline.

This module is designed to produce 512x512 images for ML-Training.
It checks the size, if its over 1000px it crops a square out of the center
and resizes it to 512x512. All processed images are stored in a new subfolder.
"""

import os
from PIL import Image, ImageOps

folder_path = 'Media_Doc/Batch_Test/'

files = [f for f in os.listdir(folder_path) if f.endswith(('.JPG', '.jpg', '.jpeg'))]


def center_crop(img):
    """Crops the center square out of the image."""
    width, height = img.size # Take image size by width and height
    size = min(img.size)    # Detect smallest length
    left = (width - size) // 2  # Calculates left offset
    top = (height - size) // 2  # Calculates top offset
    right = left + size # Calculates right offset
    bottom = top + size # Calculates bottom offset
    return img.crop((left, top, right, bottom))

def resize_image(img_crop):
    """Resizes the image to 512x512 pixels using LANCZOS resampling."""
    img_resize = img_crop.resize((512, 512), Image.Resampling.LANCZOS)
    return(img_resize)

os.makedirs('Media_Doc/Batch_Test/Processed_Data', exist_ok=True)
new_folder_path = 'Media_Doc/Batch_Test/Processed_Data/'

for file in files:
    file_path = os.path.join(folder_path, file)
    img = Image.open(file_path)
    img = ImageOps.exif_transpose(img)
    width, height = img.size
    if width < 1000 or height < 1000:
        print("Überspringen...")
        continue
    img = center_crop(img)
    img = resize_image(img)
    new_path = os.path.join(new_folder_path, file)
    img.save(new_path)