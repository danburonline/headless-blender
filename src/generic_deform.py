import bpy
import os
from datetime import datetime

# Base directory assuming the script is run from the root directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the source and destination paths
source_blend = os.path.join(base_dir, "..", "files", "blender", "example_source.blend")
destination_folder = os.path.join(base_dir, "..", "dist")
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath=source_blend)

# Deselect all objects first to ensure a clean slate
bpy.ops.object.select_all(action="DESELECT")

# Assuming there is only one object and it's the first in the collection
obj = bpy.context.scene.objects[0]

# Select the object and make it the active object
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Scale the object
bpy.ops.transform.resize(value=(2.76192, 2.76192, 2.76192), orient_type="GLOBAL")

# Switch into edit mode
bpy.ops.object.mode_set(mode="OBJECT")
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action="DESELECT")
bpy.ops.object.mode_set(mode="OBJECT")
# obj.data.vertices[0].select = True
vertex = obj.data.vertices[0]

# move vertex to 5,1,1
vertex.co = (5, 1, 1)

bpy.ops.object.mode_set(mode="EDIT")
# move the vertex


# Make sure the destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Save the changes to a new .blend file with a timestamp
output_blend = os.path.join(
    destination_folder, f"transformed_example_{timestamp}.blend"
)
bpy.ops.wm.save_as_mainfile(filepath=output_blend)
