#! /bin/bash

# https://www.davidpashley.com/articles/writing-robust-shell-scripts
# Fail on any errors
set -e

# Build the image
docker build -t iron-gauntlet .