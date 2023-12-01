"""This script creates a red sphere and saves it to a .blend file."""
import os
import bpy

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Create a new sphere
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1, enter_editmode=False, align="WORLD", location=(0, 0, 0)
)

# Set the sphere's material to red
material = bpy.data.materials.new(name="RedMaterial")
material.diffuse_color = (1, 0, 0, 1)  # Red color
bpy.context.object.data.materials.append(material)

# Save the file
file_path = os.path.join(os.path.dirname(bpy.data.filepath), "dist/example.blend")
bpy.ops.wm.save_as_mainfile(filepath=file_path)
