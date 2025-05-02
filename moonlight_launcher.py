#!/usr/bin/env python3

# moonlight_launcher.py

import subprocess
import sys
import time

# Import variables loaded from .env by config.py
from config import HOST_IP, APP, LOG_FILE
from wake import is_host_reachable, wake_host, log

def launch_moonlight():
    """Launches the moonlight-qt command."""
    log("Launching Moonlight...")
    # Construct the moonlight command
    moonlight_cmd = [
        "moonlight-qt",
        "stream",
        "-app", APP,
        "-1080",
        "-display-mode", "fullscreen",
        "-input", "keyboardmouse",
        "--absolute-mouse",
        "--no-game-optimization",
        HOST_IP
    ]

    try:
        # Launch moonlight-qt. We'll redirect its output to the log file.
        log(f"Executing command: {' '.join(moonlight_cmd)}")
        process = subprocess.Popen(moonlight_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Read moonlight-qt's output line by line and write to the log file
        with open(LOG_FILE, "a") as log_file:
            for line in iter(process.stdout.readline, b''):
                log_file.write(line.decode('utf-8'))

        process.wait() # Wait for moonlight-qt to finish
        log(f"Moonlight exited with return code {process.returncode}.")
        return process.returncode
    except FileNotFoundError:
        log("Error: moonlight-qt command not found. Is it installed and in your PATH?")
        return 1 # Indicate an error
    except Exception as e:
        log(f"Error launching Moonlight: {e}")
        return 1 # Indicate an error

if __name__ == '__main__':
    log("Starting Moonlight Launch Script (Python)")

    # Check if the host is reachable
    if not is_host_reachable():
        log(f"Host {HOST_IP} is not reachable. Attempting Wake-on-LAN.")
        if not wake_host():
            log("Failed to send Wake-on-LAN packet. Exiting.")
            sys.exit(1) # Exit with an error code

        log("Waiting for host to come online after Wake-on-LAN...")
        time.sleep(30) # Wait longer for the host to boot

        if not is_host_reachable():
            log("Host still not reachable after Wake-on-LAN. Exiting.")
            sys.exit(1) # Exit with an error code
    else:
        log(f"Host {HOST_IP} is reachable.")

    # Launch Moonlight
    exit_code = launch_moonlight()
    sys.exit(exit_code)
