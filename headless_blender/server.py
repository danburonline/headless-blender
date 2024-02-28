"""Web server for uploading GLTF files and processing them with Blender."""
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os

from headless_blender.self_fracture import process_gltf
from zipfile import ZipFile

app = FastAPI()


@app.post("/upload-gltf/")
async def upload_gltf(zip_file: UploadFile = File(...)):
    """Upload a GLTF file and process it with Blender."""
    temp_dir = f"temp/{zip_file.filename}-unzipped"
    os.makedirs(temp_dir, exist_ok=True)
    temp_zip_path = f"{temp_dir}/{zip_file.filename}"
    with open(temp_zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    # Unzip the file
    with ZipFile(temp_zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Assume the GLTF file is named 'scene.gltf'
    gltf_file_path = os.path.join(temp_dir, "scene.gltf")
    # Process the GLTF file with your Blender function
    glb_file_path = process_gltf(gltf_file_path)

    # Process the GLTF file with your Blender function
    process_gltf(gltf_file_path)

    # Clean up: remove the temporary directory
    shutil.rmtree(temp_dir)

    return FileResponse(
        path=glb_file_path,
        filename=os.path.basename(glb_file_path),
        media_type="model/gltf-binary",
    )
