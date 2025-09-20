#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".job_tech_venv" ]; then
    python -m venv .job_tech_venv
fi

# Activate the virtual environment
source .job_tech_venv/Scripts/activate

# Upgrade pip using python -m pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Environment setup complete. To activate later, run:"
echo "source .job_tech_venv/Scripts/activate"