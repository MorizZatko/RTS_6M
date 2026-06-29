"""Mesh objects to CSV list.

This module iterates through all objects in the Blender scene to find mesh objects.
It fills a nested list with the collected data. 
Finally, it writes all values to a CSV file at a hardcoded file path.
(Notice: The code must run within an existing Blender project.)
"""

import bpy
import csv

# Initialize list
assets = []

# Find all mesh objects and append it to a nested list
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        name = obj.name
        count = len(obj.data.vertices)
        type = 'Mesh'
        assets.append([name, count, type])

# Create CSV list with all found values
with open('C://Users//moriz//Desktop//RTS//python_start//assets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Object Name', 'Vertices', 'Type'])
    writer.writerows(assets)