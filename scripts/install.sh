#! /bin/bash

# https://www.davidpashley.com/articles/writing-robust-shell-scripts
# Fail on any errors
set -e

# Install docker if not found
command -v docker || {
    echo -n "Installing docker..."
    curl -sSL https://get.docker.com | sh
    echo "done."
    
    # Add current user to docker group
    echo -n "Performing post-installation steps..."
    sudo usermod -aG docker $USER
    echo "done."
}

# Build the image
echo -n "Building docker image..."
BASEDIR=$(dirname "$0")
pushd $BASEDIR
docker build -t iron-gauntlet ..
popd
echo "done."

# Run the container in the backgrond and have it restart always
echo -n "Installing container as daemon..."
docker run --name iron-gauntlet-daemon -d --restart always --privileged --network host -it iron-gauntlet
echo "done."