"""Blender random cube generator.

This module generates a random number of cubes in a random positions without intersecting each other.
The cube count ranges from 5 to 25, X/Y positions range from 0 to 10.
Finally, each cube gest its own numerical name.
"""

import bpy
import random
from mathutils import Vector

# Generate a random target count of cubes to create
cube_count_rnd = random.randint(5, 25)

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

        # Try to find a valid coordinate that does not collide
        while no_touch((loc_rnd_x, loc_rnd_y, 0)) and attemps < 100:
            loc_rnd_x = random.randint(0, 10)
            loc_rnd_y = random.randint(0, 10)
            attemps += 1

        # Spawn the cube if a valid position was found within 100 attempts
        bpy.ops.mesh.primitive_cube_add(location=(loc_rnd_x, loc_rnd_y, 0))
        obj = bpy.context.active_object
        obj.type == "MESH"
        obj.name = f"Cube{i+1:02d}"

# Run the generator function
generate_random_cubes(cube_count_rnd)