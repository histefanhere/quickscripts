#!/bin/sh
# run.sh - run the quickscripts program.
# This script is meant to be executed by other programs, such as
# xbindkeys.
# AUTHOR: Stefan Zdravkovic

# Leave this script in the `hotkeys` directory

# Get to this scripts directory
cd "$(dirname "$(readlink -f "$0")")"

# Go out one to get to the repo's root directory...
cd ..

# And execute the python script
/usr/bin/env python3 main.py
