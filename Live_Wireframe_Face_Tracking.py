"""Live Wireframe Face Tracking.

This module reads a live video input, resizes it, and converts it to RGB color space.
It detect a face to place wireframe landmarks and draws a red circle on the nose.
Finally, the result is displayed live until 'q' key is pressed.
"""


import cv2
import mediapipe as mp


# Initialize video input
cam = cv2.VideoCapture(0)

# Initialize values for resizing
scale = 0.3
mult = 1 / scale

# Initialize face mesh via mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Start process loop
while True:

    # Get video informations
    ret, frame = cam.read()
    if not ret:
        print('Camera not found...')
        break

    # Get input frame dimensions
    h, w, c = frame.shape

    # Resize and color space convertion process
    cam_resize = cv2.resize(frame, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
    cam_rgb = cv2.cvtColor(cam_resize, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(cam_rgb)

    # Process detected face landmarks
    if results.multi_face_landmarks:

        # Draw wireframe for each face
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image = frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
            
        # Extract nose tip landmark index
        nose = face_landmarks.landmark[1]

        # Calculate pixel position for the original frame
        px = int(nose.x * w)
        py = int(nose.y * h)

        # Draw red circle at the the nose position
        cv2.circle(frame, (px, py), 50, (0, 0, 255), -1)


    # Display final live video
    cv2.imshow('Webcam-Live', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break