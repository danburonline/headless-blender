from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os
from zipfile import ZipFile
import subprocess
from pathlib import Path

app = FastAPI()


def find_latest_glb_file(directory: str) -> str:
    """Find the most recently created .glb file in the specified directory."""
    list_of_files = Path(directory).glob("*.glb")
    latest_file = max(list_of_files, key=os.path.getctime, default=None)
    return str(latest_file) if latest_file else None


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
    blender_script_path = "./headless_blender/blender_process.py"

    # Call Blender in headless mode to process the GLTF file
    subprocess.run(
        [
            blender_executable_path,
            "--background",
            "--python",
            blender_script_path,
            "--",
            gltf_file_path,
        ],
        check=True,
    )

    # Find the most recently created GLB file in the correct directory
    dist_directory = (
        "/app/headless_blender/dist"  # Updated to match Blender script output
    )
    glb_file_path = find_latest_glb_file(dist_directory)

    if not glb_file_path or not os.path.exists(glb_file_path):
        return {"error": "GLB file not found."}

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
