"""OpenCV Cascades.

This module reads a hardcoded JPG file, resizes it, and converts it to the gray-scale color space.
It detects faces and eyes via 'haarcascade_frontface_default.xml' and 'haarcascade_eye.xml',
using the Cascade-Classifier. For ever detected face, and every eye within that face, 
it draws a green rectangle onto the resized image.
Finally, it displays the result, waiting for a key to get pressed to end the process.
"""

import cv2

# Load image, resize it and convert it to gray-scale
img  =  cv2.imread(r'C:\Users\moriz\Desktop\RTS\python_start\Media_Doc\Buntspecht_Salzhaus-06356.JPG')
img_resize = cv2.resize(img, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
img_gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)

# Load and initialize face and eye detection via XML files
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Start face detection process
find_face = face_cascade.detectMultiScale(img_gray, 1.1, 4)

# Starting drawing and eye detection loop
for (x, y, w, h) in find_face:

    # Crop the region of interest and start eye detection process
    roi_crop = img_gray[y:y+h, x:x+w]
    find_eye = eye_cascade.detectMultiScale(roi_crop, 1.1, 3)

    # Draw rectangle for every found face
    cv2.rectangle(img_resize, (x, y), (x + w, y + h), (0, 255, 128), 2)

    # Draw rectangle for every found eye
    for (ex, ey, ew, eh) in find_eye:
        cv2.rectangle(img_resize, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 128), 2)

# Display the result
cv2.imshow("Test", img_resize)
cv2.waitKey(0)
cv2.destroyAllWindows()