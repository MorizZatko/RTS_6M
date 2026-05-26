"""Augmentation Generator.

This module reads all JPG images in the source folder and applies different image transformations
(mirroring, flipping, rotating, contrast and greyscale) to generate seperate images.
"""

import os
from PIL import Image, ImageOps, ImageEnhance

path = 'Media_Doc/Augment_Test/'
img_file = [f for f in os.listdir(path) if f.endswith('.JPG')]
os.makedirs('Media_Doc/Augment_Test/Augmented_Data/', exist_ok=True)
new_folder_path = 'Media_Doc/Augment_Test/Augmented_Data'


def Image_Transpose_Mirr(img):
    """Mirrors the image."""
    return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 
def Image_Transpose_Vert(img):
    """Flips the image vertically."""
    return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
def Image_Transpose_Rota(img):
    """Rotates image by 90 degrees."""
    return img.transpose(Image.Transpose.ROTATE_90)
       
def Image_Contrast(img):
    """Enhances the contrast of the image."""
    cont_enhancer = ImageEnhance.Contrast(img)
    return cont_enhancer.enhance(2.25)
        
def Image_Desaturation(img):
    """Converts image to greyscale."""
    sat_enhancer = ImageEnhance.Color(img)
    return sat_enhancer.enhance(0)

for file in img_file:
    file_path = os.path.join(path, file)
    file_split = file.split('.')
    img = Image.open(file_path)
    img = ImageOps.exif_transpose(img)

    orginal_name = file_split[0]
    file_type = file_split[1]

    tran_Mirr = Image_Transpose_Mirr(img)
    tran_Vert = Image_Transpose_Vert(img)
    tran_Rota = Image_Transpose_Rota(img)
    cont = Image_Contrast(img)
    desa = Image_Desaturation(img)

    tran_Mirr_name = f"flip_mirr_{orginal_name}.{file_type}"
    tran_Vert_name = f"flip_vert_{orginal_name}.{file_type}"
    tran_Rota_name = f"flip_rota_{orginal_name}.{file_type}"
    cont_name = f"cont_{orginal_name}.{file_type}"
    desa_name = f"desa_{orginal_name}.{file_type}"

    tran_Mirr_path = os.path.join(new_folder_path, tran_Mirr_name)
    tran_Vert_path = os.path.join(new_folder_path, tran_Vert_name)
    tran_Rota_path = os.path.join(new_folder_path, tran_Rota_name)
    cont_path = os.path.join(new_folder_path, cont_name)
    desa_path = os.path.join(new_folder_path, desa_name)

    tran_Mirr.save(tran_Mirr_path)
    tran_Vert.save(tran_Vert_path)
    tran_Rota.save(tran_Rota_path)
    cont.save(cont_path)
    desa.save(desa_path)