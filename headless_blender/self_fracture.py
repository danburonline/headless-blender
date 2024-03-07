import os
from datetime import datetime
import bpy


def process_gltf(gltf_file_path):
    """Process a GLTF file"""
    # Create an empty Blender file
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=gltf_file_path)

    imported_object = None
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            imported_object = obj
            break

    if not imported_object:
        raise ValueError("No imported mesh found")

    # Move the object up
    x, y, z = imported_object.location
    imported_object.location = (x, y, z + 2.0)

    # Apply the scale
    bpy.ops.object.transform_apply(scale=True)

    # Ensure the Cell Fracture addon is enabled
    bpy.ops.preferences.addon_enable(module="object_fracture_cell")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # Process each object in the scene
    for obj in bpy.data.objects:
        obj.select_set(True)
        x, y, z = obj.location
        obj.location = (x, y, z + 3.0)

        # Make the object the active object
        bpy.context.view_layer.objects.active = obj

        # Apply Cell Fracture
        bpy.ops.object.add_fracture_cell_objects()  # type: ignore

        # Store the name of the original object
        original_obj_name = obj.name

        # Deselect all objects
        bpy.ops.object.select_all(action="DESELECT")

        # Select and delete the original object
        bpy.data.objects[original_obj_name].select_set(True)
        bpy.ops.object.delete()

    # Find the first mesh object, which will be your imported GLTF, to set as active
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            bpy.context.view_layer.objects.active = obj  # Set the mesh object as active
            break

    if bpy.context.active_object is not None:
        original_obj_name = bpy.context.active_object.name
    else:
        raise ValueError(
            "No active mesh object found. Please ensure the GLTF file was imported correctly."
        )

    # Apply rigid body to fractured pieces
    for obj in bpy.data.objects:
        # The fractured pieces should have the original object's name as part of their new name
        if original_obj_name in obj.name:
            bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
            obj.select_set(True)  # Select the current object
            bpy.context.view_layer.objects.active = obj  # Set as the active object
            bpy.ops.rigidbody.object_add()  # Add active rigid body
            obj.rigid_body.type = "ACTIVE"  # Set rigid body to active
            obj.rigid_body.collision_shape = "MESH"  # Set collision shape to MESH

    # Add a plane at the center
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0)
    )

    # Scale up the plane
    plane = bpy.context.active_object
    plane.scale = (5, 5, 5)

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

    # Remove the plane
    bpy.data.objects.remove(plane, do_unlink=True)

    # Get the directory where the blend file is located
    blend_file_directory = os.path.dirname(bpy.data.filepath)

    # If the blend file is not saved, use the current directory
    if not blend_file_directory:
        blend_file_directory = os.path.dirname(os.path.realpath(__file__))

    # Ensure the 'dist' directory exists
    dist_directory = os.path.join(blend_file_directory, "dist")
    os.makedirs(dist_directory, exist_ok=True)

    # Get current date and time for the file name
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define the GLB export path with the current date and time
    glb_export_path = os.path.join(
        dist_directory, f"animated_fracture_{current_datetime}.glb"
    )

    # Export to GLB with animations
    bpy.ops.export_scene.gltf(
        filepath=glb_export_path,
        export_format="GLB",
        use_selection=False,  # Export all objects in the scene
        export_apply=True,  # Apply modifiers and other settings
        export_animations=True,  # Include animations
        export_frame_range=True,  # Use the current frame range
        export_frame_step=1,  # Export all frames
    )

    print(f"Exported GLB file to {glb_export_path}")

    return glb_export_path
