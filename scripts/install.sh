#! /bin/bash

# https://www.davidpashley.com/articles/writing-robust-shell-scripts
# Fail on any errors
set -e

# Build the image
docker build -t iron-gauntlet .

# Run the container in the backgrond and have it restart always
docker run --name iron-gauntlet-daemon -d --restart always --privileged --network host -it iron-gauntlet