import bpy

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath="example.blend")

# Deselect all objects first to ensure a clean slate
bpy.ops.object.select_all(action="DESELECT")

# Assuming there is only one object and it's the first in the collection
obj = bpy.context.scene.objects[0]

# Select the object and make it the active object
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Scale the object
bpy.ops.transform.resize(value=(2.76192, 2.76192, 2.76192), orient_type="GLOBAL")

# switch into edit mode
bpy.ops.object.editmode_toggle()

# select a random vertex
# TODO This doesn't work
bpy.ops.mesh.select_random(ratio=0.5, seed=0, action="SELECT")

# move this vertex randomly in 3d space
bpy.ops.transform.translate(value=(0.0, 0.0, 0.0), orient_type="GLOBAL")

# Save the changes to a new .blend file
bpy.ops.wm.save_as_mainfile(filepath="modified_example.blend")
