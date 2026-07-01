"""Mesh objects to CSV list.

This module iterates through all objects in the Blender scene to find mesh objects.
It fills a list with dictionaries containing the collected data. 
Finally, it writes all values to a CSV file at a hardcoded file path.
(Notice: The code must run within an existing Blender project.)
"""

import bpy
import csv

# Initialize list
assets = []

# Find all mesh objects and append their data as dictionaries to the list
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        name = obj.name
        count = len(obj.data.vertices)
        type = 'Mesh'
        assets.append({"Object Name": name, "Vertices": count, "Type": type})

# Create CSV list with all found values
with open('C://Users//moriz//Desktop//RTS//python_start//assets.csv', 'w', newline='') as f:
    head_field = ['Object Name', 'Vertices', 'Type']
    writer = csv.DictWriter(f, fieldnames=head_field)
    writer.writeheader()
    writer.writerows(assets)