#!/bin/bash

# Exit the script on any command failure
set -e
pip install uv
# Step 1: Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
else
    echo "Virtual environment already exists."
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."

source .venv/bin/activate

# Step 3: Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
uv pip install -r requirements.txt


