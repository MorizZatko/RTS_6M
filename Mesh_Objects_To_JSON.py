"""Mesh objects to a JSON file.

This module iterates through all objects in the Blender scene to find mesh objects.
All collected data is stored in a dictionary structure.
Finally, it writes all values to a JSON file at a hardcoded file path.
(Notice: The code must run within an existing Blender project.)
"""

import bpy
import json
import os

# Initialize list
assets = []

# Find all mesh objects and append their data as dictionaries to the list
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        name = obj.name
        count = len(obj.data.vertices)
        type = 'Mesh'
        location = obj.matrix_world.translation
        assets.append({"Object Name": name, "Vertices": count, "Type": type, "Location": [location.x, location.y, location.z]})

# Initializing dictionary base structure with dynamic name and asset values     
project_path = bpy.data.filepath
project_name = os.path.basename(project_path)
scene_data = {
    "metadata": {"author": "Moriz", "version": 3.0},
    "scene_name": project_name, "objects": assets
    }

# Create JSON file with all found values, stored as dictionaries
with open('C://Users//moriz//Desktop//RTS//python_start//scene.json', 'w') as f:
    json.dump(scene_data, f, indent=4)