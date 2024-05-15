#!/bin/bash

# Working Directory
cd /data

# Install Python Dependancies
pip install -r requirements.txt

# Run the main app
uvicorn main:app --host 0.0.0.0