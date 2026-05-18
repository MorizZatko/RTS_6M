from PIL import Image, ImageOps

base_img_1 = Image.open('Media_Doc/_MOZ4902.jpg')
base_img_1 = ImageOps.exif_transpose(base_img_1)
base_img_2 = Image.open('Media_Doc/_MOZ4903.jpg')
base_img_2 = ImageOps.exif_transpose(base_img_2)
new_image = Image.new('RGB', (10304, 7728), color=255)

new_image.paste(base_img_1, (0, 0))
new_image.paste(base_img_2, (5152, 0))

new_image.save('Media_Doc/Pillow_Comp_1.jpeg')
new_image.show()