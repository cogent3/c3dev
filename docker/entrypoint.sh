#!/bin/bash

# Set the path to the SSH private key
SSH_PRIVATE_KEY=/root/.ssh/id_rsa

# Check if the SSH private key file exists
if [ -f "${SSH_PRIVATE_KEY}" ]; then
    # Set permissions
    chmod 600 "${SSH_PRIVATE_KEY}"
    # make sure that agent is running and has the key
    eval "$(ssh-agent -s)"
    ssh-add /root/.ssh/id_rsa
else
    echo "No SSH private key found at: ${SSH_PRIVATE_KEY}"
    echo "If you don't mount your SSH private key when you run the container, you won't be able to access private repositories on github."
fi

# Make sure we have the venv loaded
source /c3dev/bin/activate

# Install the local clone of cogent3
python3 -m pip install /cogent3

# Execute the main process
exec "$@"
