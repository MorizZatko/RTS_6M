"""Atlas Generator.

This module reads images from a source directory, normalizes their orientation,
and arranges up to 16 images of a identical size and color mode into a single file 4x4 grid.
"""

import os
from PIL import Image, ImageOps

source = 'Media_Doc/Batch_Test/Processed_Data/'
img_files = [f for f in os.listdir(source)]

x_length = 4 * 512
y_length = 4 * 512
atlas = Image.new('RGB', (x_length, y_length), color=255)

for index, file in enumerate(img_files):
    file_path = os.path.join(source, file)
    img = Image.open(file_path)
    img = ImageOps.exif_transpose(img)
    col = index % 4
    row = index // 4
    x = col * 512
    y = row * 512
    atlas.paste(img, (x, y))

atlas.save('Media_Doc/Atlas_1.JPG')
atlas.show()