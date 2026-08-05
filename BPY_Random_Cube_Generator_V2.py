"""Blender random cube generator version 2.

This module generates a random number of cubes in a random positions without intersecting each other.
The cube count ranges from 5 to 25, X/Y positions range from 0 to 10.
Each cube receives a new material with a random color at full opacity.
Finally, each cube gest its own numerical name, and a point light source is placed at a random position (X/Y: 0 to 10, Z: 5 to 10).
"""

import bpy
import random
from mathutils import Vector

# Generate a random target count of cubes to create
cube_count_rnd = random.randint(5, 25)

def no_touch(new_loc, threshold=2.0):
    """Check if the new location is too close to existing mesh objects."""
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
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

        # Try to find a valid coordinate that does not collide
        while no_touch((loc_rnd_x, loc_rnd_y, 0)) and attemps < 100:
            loc_rnd_x = random.randint(0, 10)
            loc_rnd_y = random.randint(0, 10)
            attemps += 1

        # Spawn the cube if a valid position was found within 100 attempts
        bpy.ops.mesh.primitive_cube_add(location=(loc_rnd_x, loc_rnd_y, 0))

        # Setup new material
        mat = bpy.data.materials.new(name="RandomMat")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Get random color for the new material
        nodes["Principled BSDF"].inputs['Base Color'].default_value = (random.random(), random.random(), random.random(), 1.0)

        # Rename each cube
        obj = bpy.context.active_object
        obj.name = f"Cube{i+1:02d}"

        # Assigning material to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Generate random coordinates for the point light
lg_rnd_x = random.randint(0, 10)
lg_rnd_y = random.randint(0, 10)   
lg_rnd_z = random.randint(5, 10)     

# Spawn point light on random position
light = bpy.ops.object.light_add(type='POINT', location=(lg_rnd_x, lg_rnd_y, lg_rnd_z))

# Setup light power and color
light_obj = bpy.context.active_object
light_obj.data.energy = 1000
light_obj.data.color = (1, 1, 1)

# Run the generator function
generate_random_cubes(cube_count_rnd)