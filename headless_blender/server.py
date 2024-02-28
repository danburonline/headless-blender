from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os
from zipfile import ZipFile
import subprocess

app = FastAPI()

@app.post("/upload-gltf/")
async def upload_gltf(zip_file: UploadFile = File(...)):
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

    # Define the path to the Blender executable and your script
    blender_executable_path = "/usr/local/blender/blender"
    blender_script_path = "./blender_process.py"

    # Call Blender in headless mode to process the GLTF file
    subprocess.run([blender_executable_path, "--background", "--python", blender_script_path, "--", gltf_file_path], check=True)

    # Define the path to the output file (you'll need to ensure your Blender script outputs to a known location)
    glb_file_path = "/files/glb/file.glb"  # Update this path based on your Blender script's output

    # Clean up: remove the temporary directory
    shutil.rmtree(temp_dir)

    return FileResponse(
        path=glb_file_path,
        filename=os.path.basename(glb_file_path),
        media_type="model/gltf-binary",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}