#!/bin/bash

# Activate the virtual environment
source ./.env/Scripts/activate  # Assuming the virtual environment is in the same folder

# Run the Python file
python spreadjsoninator.py  # Assuming script.py is in the same folder as the shell script

# Deactivate the virtual environment
deactivate