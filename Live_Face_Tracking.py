"""Live Face Tracking.

This module reads a live video input, resizes it, and converts it to the gray-scale color space.
It detects faces and eyes via 'haarcascade_frontface_default.xml' and 'haarcascade_eye.xml',
using the Cascade-Classifier. For ever detected face, and every eye within that face, 
it draws a green rectangle onto the resized image.
Finally, it displays the result, waiting for the 'q' key to get pressed to end the process.
"""


import cv2

# Initialize video input
cam = cv2.VideoCapture(0)

# Setup CascadeClassifiers with XML files
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize values for resizing
scale = 0.3
mult = 1 / scale

# Start process loop
while True:

    # Get video informations
    ret, frame = cam.read()
    if not ret:
        print('Camera not found...')
        break

    # Resize and color space convertion process
    cam_resize = cv2.resize(frame, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
    cam_gray = cv2.cvtColor(cam_resize, cv2.COLOR_BGR2GRAY)

    # Start face detection process
    find_face = face_cascade.detectMultiScale(cam_gray, 1.1, 4)

    # Starting drawing and eye detection loop
    for (x, y, w, h) in find_face:

        # Draw rectangle for every found face
        cv2.rectangle(frame, (int(x*mult), int(y*mult)), (int((x+w)*mult), int((y+h)*mult)), (0, 255, 128), 2)

        # Crop the region of interest and start eye detection process
        roi_crop = cam_gray[y:y+h, x:x+w]
        find_eye = eye_cascade.detectMultiScale(roi_crop, 1.1, 4)

        # Draw rectangle for every found eye
        for (ex, ey, ew, eh) in find_eye:
            start = (int((x + ex) * mult), int((y + ey) * mult))
            end = (int((x + ex + ew) * mult), int((y + ey + eh) * mult))

            cv2.rectangle(frame, start, end, (0, 255, 128), 2)
            
    # Display final live video with head and eye tracking
    cv2.imshow('Webcam-Live', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break