"""Blender receiver.

This module receives binary coordinates from a sender script via a UDP socket.
It binds to local adress "127.0.0.1" on port 5005 and prints income data to the Blender system console.
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5005))
while True:
    data, adress = sock.recvfrom(1024)
    print(f"Recieved: {data.decode('utf-8')}")