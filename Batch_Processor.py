"""Batch Processor.

This module 
"""

import os
from PIL import Image

folder_path = 'Media_Doc/Batch_Test/'

files = [f for f in os.listdir(folder_path) if f.endswith('.JPG')]

os.makedirs('Media_Doc/Batch_Test/Processed_Data', exist_ok=True)
new_folder_path = 'Media_Doc/Batch_Test/Processed_Data/'

for file in files:
    file_path = os.path.join(folder_path, file)
    file_split = file.split('.')
    orginal_name = file_split[0]
    RGB_name = f"{orginal_name}_RGB"
    file_type = file_split[1]
    new_name = f"{RGB_name}.{file_type}"
    new_path = os.path.join(new_folder_path, new_name)
    
    img = Image.open(file_path)
    img = img.convert('RGB')
    img.save(new_path)

    print(new_path)