# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  wget \
  xz-utils \
  libjpeg-dev \
  libopenexr-dev \
  libpng-dev \
  libtiff-dev \
  libxxf86vm1 \
  libdbus-1-3 \
  libblosc1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Blender
RUN mkdir /usr/local/blender && \
  wget -O blender.tar.xz https://download.blender.org/release/Blender4.0/blender-4.0.0-linux-x64.tar.xz && \
  tar -xf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
  rm blender.tar.xz

# Add Blender to the PATH
ENV PATH="/usr/local/blender:${PATH}"

# Install Poetry version 1.7.1
RUN pip install poetry==1.7.1

# Configure Poetry: Do not create a virtual environment
RUN poetry config virtualenvs.create false

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies using Poetry
RUN poetry install --no-root --only main

# Copy the rest of your project files into the container
COPY . /app

# Expose port to access the server
EXPOSE 8000

# Run Uvicorn with live auto-reload
CMD ["uvicorn", "headless_blender.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
