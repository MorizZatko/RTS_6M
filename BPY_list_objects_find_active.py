"""BPY list all objects an find the selected.

This module iterates through a Blender scene, collects metadata for all objects and stores them in a JSON file.
Finally, it prints the selected object, if one is selected and stores the JSON file into a hardcoded directory.
"""

import bpy
import json
import os

# Initialize the list
assets = []

# Find all objects and append their data as dictionaries to the list
for obj in bpy.data.objects:
    name = obj.name
    if obj.type == 'MESH':
        count = len(obj.data.vertices)
    else:
        count = None
    type = obj.type
    location = obj.matrix_world.translation
    assets.append({"Object Name": name, "Vertices": count, "Type": type, "Location": [location.x, location.y, location.z]})

# Find selected active object
if bpy.context.active_object:
    print(f"{bpy.context.active_object.name} is selected")
else:
    print("No object is selected")

# Setup main structure for the JSON  
project_path = bpy.data.filepath
project_name = os.path.basename(project_path)
scene_data = {
    "metadata": {"author": "Moriz", "version": 3.0},
    "scene_name": project_name, "objects": assets
    }

# Create CSV list with all found values
with open('C://Users//moriz//Desktop//RTS//python_start//scene.json', 'w') as f:
    json.dump(scene_data, f, indent=4)