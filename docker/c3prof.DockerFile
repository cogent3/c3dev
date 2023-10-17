# Use Debian as a base image
FROM debian:latest

# Set environment variables to ensure non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    curl \
    graphviz \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /c3env/lib/python3.11/site-packages/cogent3

# Create a Python virtual environment and activate it
RUN python3.11 -m venv /c3env
ENV PATH="/c3env/bin:$PATH"

# Install cogent3 from GitHub
RUN pip install "cogent3[dev]"

# Install pytest, pytest-profiling and other required Python packages
RUN python -m pip install pytest pytest-profiling gprof2dot

# Default command to run pytest with profiling
CMD ["pytest", "--profile", "--profile-svg", "--pstats-dir=/results"]
