#!/bin/bash

echo "PROTEUS: v1.0.0-alpha.1"

# Initialize variables
python_executable=

# Check if either 'python' or 'python3' is installed
if command -v python > /dev/null 2>&1; then
    python_executable=python
elif command -v python3 > /dev/null 2>&1; then
    python_executable=python3
fi

if [ -n "$python_executable" ]; then
    echo "PROTEUS: $python_executable is installed on your system."
    echo "PROTEUS: Installed Python version:"
    $python_executable --version || true
else
    echo "PROTEUS: Neither 'python' nor 'python3' is installed on your system."
    echo "PROTEUS: Please install Python and try running this script again. Recommended version: 3.10.7"
    exit 1
fi

script_dir="$(dirname "$0")"
venv_dir="$script_dir/proteus_env"

echo "PROTEUS: Checking for the existence of virtual environment 'proteus_env'"
if [ -d "$venv_dir" ]; then
    echo "PROTEUS: Environment 'proteus_env' was found."
else
    echo "PROTEUS: Environment 'proteus_env' was not found."
    echo "PROTEUS: Creating a virtual environment using $python_executable..."

    $python_executable -m venv "$venv_dir"
    
    if [ -d "$venv_dir" ]; then
        echo "PROTEUS: Virtual environment created successfully."
    else
        echo "PROTEUS: Failed to create the virtual environment."

        # If failed to create the venv, show the error message and exit
        exit 1
    fi
fi

echo "PROTEUS: Activating the virtual environment..."
source "$venv_dir/bin/activate"

echo "PROTEUS: Installing the required packages..."
pip install -r "$script_dir/requirements.txt"

# Run the application in the background so the console can be closed
echo "PROTEUS: Running the application..."
$python_executable -m proteus &
