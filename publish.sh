#!/bin/bash

# Run Python file
python3 spreadjsoninator.py

# Git commands
git add .
git commit -m "Auto commit: $(date +"%Y-%m-%d %H:%M:%S")"
git push