"""Blender live tracker and sender.

This module sends binary coordinates to blender via a UDP socket to server address "127.0.0.1" on port 5005.
Using Computer Vision and a webcam, it tracks a red object, draws a red circle onto the tracked center point, and sends the normalized coordinates to Blender.
"""

import socket
import cv2

def map_value(value, in_min, in_max, out_min, out_max):
    """Normalize pixel values into normalized coordinates."""
    norm = (value - in_min) / (in_max - in_min)
    scaled = out_max - out_min
    sc_norm = norm * scaled
    offset = sc_norm + out_min
    return offset

# Setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5005)

# Initialize camera
cam = cv2.VideoCapture(0)

# Blender min and max values
B_min = -5
B_max = 5

while True:
    ret, frame = cam.read()

    # Get the shape of the video input
    height, width, channels = frame.shape

    # Color convertion and masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)

        # Calculate and send coordinates to Blender
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Draw circle onto the tracked area
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Calculate normalized coordinates by the "map_value" function
            blender_x = map_value(cx, 0, width, B_min, B_max)
            blender_y = map_value(cy, 0, height, B_min, B_max)

            message = f"{blender_x},{blender_y}".encode('utf-8')
            sock.sendto(message, server_address)

    # Show live view and ends it by pressing "q"
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()




