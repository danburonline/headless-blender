# Headless Blender

This repository is an experimental side project to determine the feasibility of running Blender in headless mode, without a graphical user interface (GUI), while still being able to render images and run simulations.

## Quick Start

1. Open the project via the Poetry shell: `poetry shell`
2. Install the project dependencies: `poetry install`
3. Run the example server: `uvicorn headless_blender.server:app --reload`
4. Import the [API specs](./docs/api/specs.json) into Hoppscotch and use the API accordingly
