"""Blender Material Builder.

Thius script automates the creation of a Blender material by a texture metadata from a JSON file.
It sets up a node tree with Principled BSDF, Diffuse, Roughness and Normal maps with correct color spaces.
"""

import json
import os
import bpy

# Define path for the asset metadata
meta_path = r"C:\Users\moriz\Desktop\RTS\python_start\Media_Doc\Downloads\PolyHeaven\aerial_asphalt_01\metadata.json"
meta_dir = os.path.dirname(meta_path)

# Load metadata from JSON file
with open(meta_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)
    
print("Asset-Name:", metadata["name"])
print("Diffuse Pfad:", metadata["local_files"]["diffuse"])

# Get or create the material with matching asset name
mat_name = metadata["name"]
material = bpy.data.materials.get(mat_name) or bpy.data.materials.new(name=mat_name)

# Clear existing nodes to ensure a fresh setup
nodes = material.node_tree.nodes
nodes.clear()

print(f"\nMaterial '{mat_name}' wurde erstellt!")
for node in nodes:
    print(f"-> Node im Shader: {node.name} (Typ: {node.type}")

# Create core shader setup nodes
output_node = nodes.new(type="ShaderNodeOutputMaterial")
principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
principled_node.location, output_node.location = (0, 0), (300, 0)


if principled_node and output_node:
    print(f"[Blender API] Beide standard nodes wurden erfolgreich geprüft!")
    print(f"Principled BSDF Position: {principled_node.location}")
    
# --- Setup Diffuse Map ---
diff_node = nodes.new(type="ShaderNodeTexImage")
diff_node.location = (principled_node.location.x -400, principled_node.location.y +200)
diff_node.label = "Diffuse Map"

# Resolve path, load image and assign to node
diff_filename = os.path.basename(metadata["local_files"]["diffuse"])
diff_path = os.path.join(meta_dir, diff_filename)
loaded_img_diff = bpy.data.images.load(diff_path)
diff_node.image = loaded_img_diff

print(f"\n[Blender API] Diffuse-Bild '{loaded_img_diff.name}' erfolgreich geladen!")

# Link Diffuse to Base Color
links = material.node_tree.links
links.new(diff_node.outputs["Color"], principled_node.inputs["Base Color"])

# --- Setup Roughness Map ---
rough_node = nodes.new(type="ShaderNodeTexImage")
rough_node.location = (principled_node.location.x -400, principled_node.location.y -200)
rough_node.label = "Roughness Map"

# Resolve path, load image, convert color space to Non-Color and asign to node
rough_filename = os.path.basename(metadata["local_files"]["roughness"])
rough_path = os.path.join(meta_dir, rough_filename)
loaded_img_rough = bpy.data.images.load(rough_path)
rough_node.image = loaded_img_rough
rough_img_color = loaded_img_rough.colorspace_settings.name = 'Non-Color'

print(f"\n[Blender API] Roughness-Bild '{loaded_img_rough.name}' erfolgreich geladen!")

# Link Roughness
links = material.node_tree.links
links.new(rough_node.outputs["Color"], principled_node.inputs["Roughness"])

# --- Setup Normal Map ---
nor_img_node = nodes.new(type="ShaderNodeTexImage")
nor_img_node.location = (principled_node.location.x -400, principled_node.location.y -500)
nor_img_node.label = "Normal IMG Map"

# Resolve path, load image, convert color space to Non-Color and asign to node
nor_img_filename = os.path.basename(metadata["local_files"]["normal"])
nor_img_path = os.path.join(meta_dir, nor_img_filename)
loaded_img_nor = bpy.data.images.load(nor_img_path)
nor_img_node.image = loaded_img_nor
nor_img_color = loaded_img_nor.colorspace_settings.name = 'Non-Color'

# Create Normal Map node
nor_map_node = nodes.new(type="ShaderNodeNormalMap")
nor_map_node.location = (principled_node.location.x -100, principled_node.location.y -500)
nor_map_node.label = "Normal Map"

print(f"\n[Blender API] Normal-Bild '{loaded_img_nor.name}' erfolgreich geladen!")

# Link Normal Image through Normal Map node to Principled BSDF
links = material.node_tree.links
links.new(nor_img_node.outputs["Color"], nor_map_node.inputs["Color"])
links.new(nor_map_node.outputs["Normal"], principled_node.inputs["Normal"])