# Use the Python base image
FROM --platform=linux/amd64 python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install wget, xz-utils, and necessary libraries for Blender
# Install necessary libraries for Blender, wget, xz-utils, and libSM
RUN apt-get update && apt-get install -y \
  wget \
  xz-utils \
  libxi6 \
  libxrender1 \
  libxfixes3 \
  libgl1 \
  libdbus-1-3 \
  libxkbcommon0 \
  libsm6 \
  && rm -rf /var/lib/apt/lists/*

# Download and install Blender
RUN mkdir /usr/local/blender && \
  wget -O blender.tar.xz https://download.blender.org/release/Blender4.0/blender-4.0.0-linux-x64.tar.xz && \
  tar -xf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
  rm blender.tar.xz


# Add Blender to the PATH
ENV PATH="/usr/local/blender:${PATH}"

# Install Poetry for managing dependencies
RUN pip install poetry==1.7.1

# Configure Poetry: Do not create a virtual environment
RUN poetry config virtualenvs.create false

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies using Poetry
RUN poetry install --no-root --only main

# Copy the rest of your project files into the container
COPY . /app

RUN mkdir /app/dist

# Expose port to access the FastAPI server
EXPOSE 8000

# Run the server via Uvicorn
CMD ["uvicorn", "headless_blender.server:app", "--host", "0.0.0.0", "--port", "8000"]
