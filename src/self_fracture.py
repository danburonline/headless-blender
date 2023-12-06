"""Example Python headless file"""
import os
import subprocess
from datetime import datetime
import bpy


# Create an empty Blender file
bpy.ops.wm.read_factory_settings(use_empty=True)


# Load a GLTF file
def load_gltf(file_path):
    bpy.ops.import_scene.gltf(filepath=file_path)


gltf_file_path = "./src/scene.gltf"
load_gltf(gltf_file_path)

imported_object = None
for obj in bpy.data.objects:
    if obj.type == "MESH":
        imported_object = obj
        break

if not imported_object:
    raise Exception("No imported mesh found")

# Move the object up
imported_object.location.z += 3.0

# Ensure the Cell Fracture addon is enabled
bpy.ops.preferences.addon_enable(module="object_fracture_cell")

# Deselect all objects
bpy.ops.object.select_all(action="DESELECT")

# Process each object in the scene
for obj in bpy.data.objects:
    obj.select_set(True)
    obj.location.z += 3.0

    # Make the object the active object
    bpy.context.view_layer.objects.active = obj

    # Apply Cell Fracture
    bpy.ops.object.add_fracture_cell_objects()

    # Store the name of the original object
    original_obj_name = obj.name

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # Select and delete the original object
    bpy.data.objects[original_obj_name].select_set(True)
    bpy.ops.object.delete()

# Iterate
for obj in bpy.data.objects:
    # Check if the object is a fractured piece
    if original_obj_name in obj.name:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = "ACTIVE"

# Add a plane at the center
bpy.ops.mesh.primitive_plane_add(
    size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0)
)

# Scale up the plane
plane = bpy.context.active_object
plane.scale = (10, 10, 10)

# Set plane as passive rigid body
bpy.ops.rigidbody.object_add()
plane.rigid_body.type = "PASSIVE"
plane.rigid_body.collision_shape = "MESH"

# Bake physics
bpy.ops.ptcache.bake_all(bake=True)

# Apply visual transform to each object and insert keyframes
for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
    bpy.context.scene.frame_set(frame)
    for obj in bpy.data.objects:
        # Only apply to fractured pieces
        if original_obj_name in obj.name:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            obj.keyframe_insert(data_path="location")
            obj.keyframe_insert(data_path="rotation_euler")
            obj.keyframe_insert(data_path="scale")

# Get current date and time
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define the file path with the current date and time appended
file_path = os.path.join(
    os.path.dirname(bpy.data.filepath), f"dist/example_{current_datetime}.blend"
)

# Save the file
bpy.ops.wm.save_as_mainfile(filepath=file_path)

# Open the saved file in Blender (optional)
blender_path = "blender"  # or the full path to the blender executable
subprocess.Popen([blender_path, file_path])
