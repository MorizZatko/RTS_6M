"""Live Tracking Alpha Channel.

This module reads a live video input, resizes it, and converts it to RGB color space.
It detects face landmarks to align and project a 2D PNG asset (with alpha channel) onto the face mesh.

Note:
    2D transformations only support roll and 2D-scaling.
    Pitch and yaw (3D rotations) couse missleading results.

Press 'q' to exit the live video preview.
"""


import cv2
import mediapipe as mp
import math


# Initialize video input
cam = cv2.VideoCapture(0)
asset = cv2.imread('Media_Doc/SciFi_Helmet.png', cv2.IMREAD_UNCHANGED)

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

    frame = cv2.flip(frame, 1)

    # Get input frame dimensions
    h, w, c = frame.shape
    asset_h, asset_w, asset_c = asset.shape

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

        # Extract key landmarks
        nose = face_landmarks.landmark[1]
        chin = face_landmarks.landmark[152]
        left_side = face_landmarks.landmark[234]
        right_side = face_landmarks.landmark[454]

        # Calculate asset dimensions
        face_w_px = int(abs(right_side.x - left_side.x) * w)
        scale_factor = face_w_px / asset_w
        scaled_w = int(asset_w * scale_factor)
        scaled_h = int(asset_h * scale_factor)
        scaled_asset = cv2.resize(asset, (scaled_w, scaled_h))

        # Calculate nose and chin position
        px_nose = int(nose.x * w)
        py_nose = int(nose.y * h)
        px_chin = int(chin.x * w)
        py_chin = int(chin.y * h)

        # Calculate roll angle between nose and chin
        angle = math.atan2(py_chin - py_nose, px_chin - px_nose)
        angle_deg = -(math.degrees(angle) - 90)

        # Rotate and scale 2D asset
        M = cv2.getRotationMatrix2D((scaled_w//2, scaled_h//2), angle_deg, 1.0)
        rotated_asset = cv2.warpAffine(scaled_asset, M, (scaled_w, scaled_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

        # Extract nose tip landmark index
        nose = face_landmarks.landmark[1]

        # Calculate pixel position for the original frame
        pos_x = int(nose.x * w) - (scaled_w // 2)
        pos_y = int(nose.y * h) - (scaled_h // 2) 

        mask = rotated_asset[:, :, 3] /  255.0

        # Alpha channel bending
        for c in range(0, 3):
            frame[pos_y:pos_y+scaled_h, pos_x:pos_x+scaled_w, c] = (1.0 - mask) * frame[pos_y:pos_y+scaled_h, pos_x:pos_x+scaled_w, c] + mask * rotated_asset[:, :, c]

    
    # Display final live video
    cv2.imshow('Webcam-Live', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break