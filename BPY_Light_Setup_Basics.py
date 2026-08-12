"""Blender light setup basics.

This module first deletes every object with "ML_" in its name.
It then creates a camera and a custom light setup, links all to the active collection,
and configures their individual parameters.
- Camera: 85mm lens, clip start/end set to 0.1 - 100.0.
- Key-Light: Area light with power 5000 and RGB color (1, 1, 1).
- Fill-Light: Point light with power 1000 and RGB color (0.8, 0.8, 1).
- Rim-Light: Spot light with power 3000 and RGB color (0.6, 0.8, 1).
"""

import bpy
import math

# Delete all objects with "ML_" in their names
for obj in bpy.data.objects:
    if "ML_" in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

# Setup camera
cam_data = bpy.data.cameras.new("Cam_Data")
cam_obj = bpy.data.objects.new("ML_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (9, -9, 7)
cam_obj.rotation_euler = (math.radians(61), 0, math.radians(45))
cam_data.lens = 85
cam_data.clip_start = 0.1
cam_data.clip_end = 100.0


def spawn_light(light_type, light_name, light_location, energy, color):
    """Spawns light objects with custom parameters and links them to the active collection.
    
    Args:
        light_type (Str): Blender light type in full caps ('POINT', 'AREA', 'Point'...)
        light_name (Str): Custom name for the new light source
        light_location (Tuple): New location for the light source (5, -7, 10)
        energy (Int): Number as int to set the light power
        color (Tuple): Light color as tuple (1, 1, 1)

    Returns:
        None.
    """
    custom_light_data = bpy.data.lights.new(f"{light_name}_Data", type=f'{light_type}')
    custom_light_obj = bpy.data.objects.new(f"ML_{light_name}", custom_light_data)
    bpy.context.collection.objects.link(custom_light_obj)
    custom_light_obj.location = light_location
    custom_light_obj.data.energy = energy
    custom_light_obj.data.color = color

# Setup light sources
spawn_light('AREA', 'Key', (0, -10, 10), 5000, (1, 1, 1))
spawn_light('POINT', 'Fill', (-10, -5, 10), 1000, (0.8, 0.8, 1))
spawn_light('SPOT', 'Rim', (10, 10, 10), 3000, (0.6, 0.8, 1))

# Rotation for the rim light
rim_light = bpy.data.objects.get("ML_Rim")
if rim_light:
    rim_light.rotation_euler = (math.radians(45), 0, math.radians(135))