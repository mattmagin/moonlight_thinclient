#!/bin/bash

# setup.sh

echo "Starting setup for Moonlight Launcher..."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# --- Flatpak Check and Installation ---
if command_exists flatpak; then
  echo "Flatpak is already installed. Proceeding with setup."
else
  read -p "Flatpak is required to install Moonlight. Do you want to install Flatpak now? (Y/n): " install_flatpak_choice
  case "$install_flatpak_choice" in
    [Yy]* )
      echo "Attempting to install Flatpak..."
      # Add commands here to install Flatpak for your distribution.
      # For Debian/Ubuntu:
      sudo apt update
      sudo apt install flatpak -y
      if [ $? -ne 0 ]; then
          echo "Error: Failed to install flatpak. Please install it manually."
          # We will still try to install the other packages, but alert the user.
          echo "Flatpak is required for Moonlight. Please install it manually to proceed with Moonlight installation."
          flatpak_installed=false
      else
          echo "Flatpak installed successfully."
          # Add the Flathub remote if you want to install apps from there (recommended for Moonlight)
          echo "Adding Flathub remote..."
          flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
          flatpak_installed=true
      fi
      ;;
    * )

      echo "Flatpak will not be installed. Please note that Flatpak is required for Moonlight to be installed."
      flatpak_installed=false

      ;;

  esac

fi

# --- End of Flatpak Check and Installation ---

# Check if pip is installed and install if not

if ! command_exists pip

then
    echo "pip not found, attempting to install python3-pip..."
    sudo apt update
    sudo apt install python3-pip -y

    if [ $? -ne 0 ]; then
        echo "Error: Failed to install python3-pip. Please install it manually."
        # We will still try to proceed with other steps
    fi
fi

# Install required Python packages system-wide using --break-system-packages

echo "Installing required Python packages (python-dotenv, ping3, wakeonlan) system-wide... "

# WARNING: Using --break-system-packages can potentially cause system instability.

# It is generally recommended to use virtual environments instead.

sudo pip install python-dotenv ping3 wakeonlan --break-system-packages

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python packages system-wide. Please check your internet connection and permissions."
    # We will still try to proceed with other steps
fi

# Make the main launcher script executable
if [ -f "moonlight_launcher.py" ]; then
    echo "Making moonlight_launcher.py executable..."
    chmod +x moonlight_launcher.py
else
    echo "Warning: moonlight_launcher.py not found in the current directory. Cannot make it executable."
fi

# --- Moonlight Flatpak Installation ---

if [ "$flatpak_installed" = true ] || command_exists flatpak; then
    echo "Attempting to install Moonlight via Flatpak..."
    # Replace with the actual Flatpak ID for Moonlight if it's different
    flatpak install flathub com.moonlight_stream.Moonlight -y
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Moonlight via Flatpak. Please check your internet connection or install it manually."
    else
        echo "Moonlight installed successfully via Flatpak."
    fi
else
    echo "Skipping Moonlight installation as Flatpak is not available."
fi

# --- End of Moonlight Flatpak Installation ---
echo "Setup complete."
