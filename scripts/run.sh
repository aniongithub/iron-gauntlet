#! /bin/bash

# https://www.davidpashley.com/articles/writing-robust-shell-scripts
# Fail on any errors
set -e

docker run --privileged --network host -it --rm iron-gauntlet