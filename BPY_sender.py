"""Blender sender.

This module sends binary coordinates to blender via a UDP socket to server adress "127.0.0.1" on port 5005.
Using a random generator, it sends new coordinate every 0.1 seconds.
"""

import socket
import random
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_adress = ('127.0.0.1', 5005)

def random_coords(counts=120):
    """Generate random coordinates and sends them to Blender."""
    message_x = 100
    message_y = 200

    for _ in range(counts):
        message_x += random.choice([-2, 0, 2])
        message_y += random.choice([-2, 0, 2])
        time.sleep(0.1)
        message = f"{message_x},{message_y}".encode('utf-8')
        sock.sendto(message, server_adress)

random_coords()
