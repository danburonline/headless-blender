# Headless Blender

This repository is an experimental side project to determine the feasibility of running Blender in headless mode, without a graphical user interface (GUI), while still being able to render images and run simulations.

## Quick Start

1. Open the project via the Poetry shell: `poetry shell`
2. Install the project dependencies: `poetry install`
3. Run the example server: `uvicorn headless_blender.server:app --reload`
4. Test the health check: `curl http://localhost:8000/health`
5. Import the [API specs](./docs/api/specs.json) into Hoppscotch and use the API accordingly

## Docker

1. Build the Docker image: `docker build -t headless-blender .`
2. Run the Docker container: `docker run -p 8000:8000 headless-blender`
3. Test the health check: `curl http://localhost:8000/health`
4. Import the [API specs](./docs/api/specs.json) into Hoppscotch and use the API accordingly
