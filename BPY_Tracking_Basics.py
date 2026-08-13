"""Blender tracking basics.

This module first deletes every object with "ML_" in its name, spawns a basic cube with "ML_" name at location (0, 0, 0).
It then creates a camera and a custom light setup, links all to the active collection,
and configures their individual parameters.
Additional it tracks the camera and spot light to the cube, to ensure fitting the view frame and a correct light setup.
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

# Spawn basic cube with custom name and location
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube_obj = bpy.context.active_object
cube_obj.name = f"ML_Cube"

# Setup camera
cam_data = bpy.data.cameras.new("Cam_Data")
cam_obj = bpy.data.objects.new("ML_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (9, -9, 7)
cam_data.lens = 85
cam_data.clip_start = 0.1
cam_data.clip_end = 100.0

# Track camera to cube object
bpy.context.view_layer.objects.active = cam_obj
constraint = cam_obj.constraints.new(type='TRACK_TO')
constraint.target = bpy.data.objects.get("ML_Cube")
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

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

# Track rim light to the cube object
rim_obj = bpy.data.objects.get("ML_Rim")
bpy.context.view_layer.objects.active = rim_obj
constraint = rim_obj.constraints.new(type='TRACK_TO')
constraint.target = bpy.data.objects.get("ML_Cube")
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Change cube location to proof tracking
cube_obj.location = (-10, -10, 5)