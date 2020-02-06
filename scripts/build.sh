#! /bin/bash

# Fail on any errors
set -e

# Build the image
BASEDIR=$(dirname "$0")
pushd $BASEDIR
docker build -t iron-gauntlet ..
popd