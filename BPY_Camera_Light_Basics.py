"""Blender camera and light basics.

This module first deletes every object with "ML_" in its name.
It then creates a camera and light, links both to the active collection,
and configures their individual parameters.
- Camera: 85mm lens, clip start/end set to 0.1 - 100.0.
- Light: Point light with power 1000 and RGB color (1, 1, 1).
"""

import bpy
import math

# Delete objects with "ML_" in their name
for obj in bpy.data.objects:
    if "ML_" in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

# Create and link camera
cam_data = bpy.data.cameras.new("Cam_Data")
cam_obj = bpy.data.objects.new("ML_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)

# Change camera location and rotation
cam_obj.location = (9, -9, 7)
cam_obj.rotation_euler = (math.radians(61), 0, math.radians(45))

# Configure camera optics
cam_data.lens = 85
cam_data.clip_start = 0.1
cam_data.clip_end = 100.0

# Create and link light
point_light_data = bpy.data.lights.new("Light_Data", type='POINT')
light_obj = bpy.data.objects.new("ML_Light", point_light_data)
bpy.context.collection.objects.link(light_obj)

# Configure light parameters and position
light_obj.data.energy = 1000
light_obj.data.color = (1, 1, 1)
light_obj.location = (5, 5, 10)