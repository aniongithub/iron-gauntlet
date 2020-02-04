#! /bin/bash

# https://www.davidpashley.com/articles/writing-robust-shell-scripts
# Fail on any errors
set -e

# Build the image
BASEDIR=$(dirname "$0")
pushd $BASEDIR
docker build -t iron-gauntlet ..
popd