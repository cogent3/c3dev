# Use the official Debian image as the base image
FROM debian:latest

# Set environment variables to non-interactive so apt-get doesn't wait for prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    openssh-client

# Set the working directory
WORKDIR /cogent3

# Create a virtual environment named c3dev
RUN python3.11 -m venv /c3dev

# Activate the virtual environment; subsequent commands will use this environment
ENV PATH="/c3dev/bin:$PATH"

# Copy entrypoint script to pass keys from the host (specified in SSH_KEYS_SOURCE_DIR) to the container
COPY docker/entrypoint.sh /entrypoint.sh

# Set permissions for the entrypoint script
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Install zsh
RUN apt-get install -y zsh

# Install oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Optionally, set zsh as the default shell for the root user
RUN chsh -s $(which zsh)

# By default run an interactive shell when the container launches
CMD ["/bin/zsh"]
