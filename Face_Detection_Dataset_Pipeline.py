"""Face Detection Dataset Pipeline.

This module reads a full dataset directory structure, for every found image file,
it converts it to the gray color space and tries to find any faces via the Cascade Classifier.
Finally, it calculates a square bounding box, crops the region, resizes it to a 224 x 224 resolution, 
and saves the output to a target directory.
"""


import os
import cv2

# Define input and output paths as well as the model path
src_folder = r'Media_Doc/lfw-deepfunneled'
target_folder = r'Media_Doc/lfw-processed'
cascade_path = r'haarcascade_frontalface_default.xml'

images = []

# Initialize the Cascade face detector
face_cascade = cv2.CascadeClassifier(cascade_path)

# Start process loop for every found picture
for root, dirs, files in os.walk(src_folder):
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png')):
            images.append(os.path.join(root, file))
            img_path = os.path.join(root, file)

            # Load original BGR image to convert it to grayscale
            org_img = cv2.imread(img_path)
            img_gray = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)

            # Detect faces to create bounding boxes
            find_face = face_cascade.detectMultiScale(img_gray, 1.1, 4)

            # Crop and export each detected face region
            for x, y, w, h,  in find_face:

                # Calculate a square crop, based on the largest dimension
                side = max(w, h)
                new_x = max(0, x - (side - w) // 2)
                new_y = max(0, y - (side - h) // 2)

                # Verify non-negative coordinates before slicing
                if not new_x < 0 or new_y < 0:

                    # Slice the square region of interest from the original color image
                    crop = org_img[new_y : new_y + side, new_x : new_x + side]

                    # Resizes crop and write it to disk
                    processed_img = cv2.resize(crop, (224, 224))
                    save_path = os.path.join(target_folder, file)
                    cv2.imwrite(save_path, processed_img)
            

print(f"Processed pictures: {len(images)}")