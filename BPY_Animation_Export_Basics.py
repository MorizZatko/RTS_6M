"""Blender animation and export basics.

This module generates a random count of cubes (5 - 15) with random colors and random locations.
Each cube is animated using keyframes to reach random target locations. The animation starts at frame 1 and
ends by frame 50. In addition to the cubes, a point light is placed randomly and a camera is created,
whose location is calculated so that every cube is within the field of view. 
Finally, the location of all cubes at frame 50 are stored in a JSON fil, and both the frame 1 and frame 50 are rendered and
saved in the same directory as the JSON file.
"""


import bpy
import random
import json
import os
from mathutils import Vector

# Generate a random target count of cubes to create
cube_count_rnd = random.randint(5, 15)

# Setup keyframe range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 50

# Create target folder for the results
render_path = r"C:\Users\moriz\Desktop\RTS\Blender\render"
os.makedirs(render_path, exist_ok=True)

def no_touch(new_loc, threshold=2.0):
    """Check if the new location is too close to existing mesh objects."""
    for obj in bpy.data.objects:
        dist = (Vector(new_loc) - Vector(obj.location)).length
        if dist < threshold:
            return True
    return False


def generate_random_cubes(cube_count_rnd):
    """Generate cubes at non-overlapping random coordinates."""
    for i in range(cube_count_rnd):
        loc_rnd_x = random.randint(0, 10)
        loc_rnd_y = random.randint(0, 10)
        attemps = 0
        while no_touch((loc_rnd_x, loc_rnd_y, 0)) and attemps < 100:
            loc_rnd_x = random.randint(0, 10)
            loc_rnd_y = random.randint(0, 10)
            attemps += 1
            
        bpy.ops.mesh.primitive_cube_add(location=(loc_rnd_x, loc_rnd_y, 0))
        
        mat = bpy.data.materials.new(name="RandomMat")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        nodes["Principled BSDF"].inputs['Base Color'].default_value = (random.random(), random.random(), random.random(), 1.0)
        
        obj = bpy.context.active_object
        obj.name = f"Cube{i+1:02d}"
        
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
            
            
def animate_cubes_random():
    """Animate mesh objects across the keyframe range with random target coordinates."""
    for obj in bpy.data.objects:
        
        loc_rnd_x = random.randint(-20, 20)
        loc_rnd_y = random.randint(-20, 20)
        loc_rnd_z = random.randint(0, 20)

        bpy.context.scene.frame_set(1)
    
        obj.keyframe_insert(data_path="location", frame=1)
    
        bpy.context.scene.frame_set(50)
    
        obj.location.x = loc_rnd_x
        obj.location.y = loc_rnd_y
        obj.location.z = loc_rnd_z
    
        obj.keyframe_insert(data_path="location", index=0, frame=50)
        
def export_metadata(filename="blender_test_metadata.json"):
    """Export coordinates of each mesh object at the current frame."""
    data = {obj.name: list(obj.location) for obj in bpy.data.objects if obj.type == 'MESH'}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
def render_frame(frame_number, render_path):
    """Render a specific frame and save the output image."""
    bpy.context.scene.frame_set(frame_number)
    bpy.context.scene.render.filepath = f"{render_path}/frame_{frame_number:03d}.png"
    bpy.ops.render.render(write_still=True)
        
# Random coordinate creation for the light source
lg_rnd_x = random.randint(0, 10)
lg_rnd_y = random.randint(0, 10)   
lg_rnd_z = random.randint(5, 10)     

# Initializing the light source
light = bpy.ops.object.light_add(type='POINT', location=(lg_rnd_x, lg_rnd_y, lg_rnd_z))

# Setup light intesity and color
light_obj = bpy.context.active_object
light_obj.data.energy = 1000
light_obj.data.color = (1, 1, 1)

# Create scene contents  
generate_random_cubes(cube_count_rnd)
animate_cubes_random()

# Calculate center point for camera positioning
locs = [obj.location for obj in bpy.data.objects if obj.type == 'MESH']
center = Vector((sum(p.x for p in locs)/len(locs),
                sum(p.y for p in locs)/len(locs),
                sum(p.z for p in locs)/len(locs)))

# Initialize camera      
bpy.ops.object.camera_add(location=(center.x + 30, center.y + 30, center.z + 30))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# Create empty object for the camera to look at
bpy.ops.object.empty_add(location=center)
target = bpy.context.active_object

# Orient the camera towards the target 
constraint = cam.constraints.new(type='TRACK_TO')
constraint.target = target
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Render first and last frame
render_frame(1, render_path)
render_frame(50, render_path)

# Create and export metadata JSON file for frame 50
bpy.context.scene.frame_set(50)
export_metadata(os.path.join(render_path, "blender_test_metadata.json"))