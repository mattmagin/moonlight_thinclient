#!/bin/bash

# setup.sh

echo "Starting setup for Moonlight Launcher..."

# Check if pip is installed and install if not
if ! command -v pip &> /dev/null
then
    echo "pip not found, attempting to install python3-pip..."
    sudo apt update
    sudo apt install python3-pip -y
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install python3-pip. Please install it manually."
        exit 1
    fi
fi

# Install required Python packages system-wide using --break-system-packages
echo "Installing required Python packages (python-dotenv, ping3, wakeonlan) system-wide... "
# WARNING: Using --break-system-packages can potentially cause system instability.
# It is generally recommended to use virtual environments instead.
sudo pip install python-dotenv ping3 wakeonlan --break-system-packages
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python packages system-wide. Please check your internet connection and permissions."
    exit 1
fi

# Make the main launcher script executable
if [ -f "moonlight_launcher.py" ]; then
    echo "Making moonlight_launcher.py executable..."
    chmod +x moonlight_launcher.py
else
    echo "Warning: moonlight_launcher.py not found in the current directory. Cannot make it executable."
fi

echo "Setup complete."
