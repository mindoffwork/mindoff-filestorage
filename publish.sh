#!/bin/bash

# Activate the virtual environment
source ./.venv/Scripts/activate  # Assuming the virtual environment is in the same folder

# Run the Python file
python spreadjsoninator.py  # Assuming script.py is in the same folder as the shell script

# Deactivate the virtual environment
deactivate

# Git commands
git add .
git commit -m "Auto commit: $(date +"%Y-%m-%d %H:%M:%S")"
git push
