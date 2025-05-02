# wake.py

import os
import sys
import time
import subprocess
from datetime import datetime
from ping3 import ping, errors
from wakeonlan import send_magic_packet

# Import variables loaded from .env by config.py
from config import HOST_IP, HOST_MAC, LOG_FILE

def log(message):
    """Appends a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%a %d %b %H:%M:%S %Z %Y")
    log_entry = f"{timestamp} - {message}\n"
    try:
        # Ensure the directory exists before writing
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True) # exist_ok=True prevents error if dir exists

        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        print(log_entry, end="") # Also print to console for immediate feedback
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE}: {e}", file=sys.stderr)
        print(log_entry, end="") # Still print to console even if logging fails


def is_host_reachable():
    """Checks if the host is reachable using ping."""
    log(f"Checking if host {HOST_IP} is reachable...")
    try:
        # ping3 returns latency in seconds or False on failure
        latency = ping(HOST_IP, timeout=1, unit='ms')
        if latency is not None and latency is not False:
            log(f"Host {HOST_IP} is reachable (latency: {latency:.2f} ms).")
            return True
        else:
            log(f"Host {HOST_IP} is not reachable.")
            return False
    except errors.PingError as e:
        log(f"Ping error: {e}")
        return False

def wake_host():
    """Sends a Wake-on-LAN packet to the host."""
    log(f"Sending Wake-on-LAN packet to {HOST_MAC}...")
    try:
        send_magic_packet(HOST_MAC)
        log("Wake-on-LAN packet sent successfully.")
        time.sleep(10) # Give the host some time to start booting
        return True
    except Exception as e:
        log(f"Error sending Wake-on-LAN packet: {e}")
        return False

if __name__ == '__main__':
    # Example usage of the functions
    if is_host_reachable():
        print("Host is currently online.")
    else:
        print("Host is offline. Attempting to wake...")
        if wake_host():
            print("WOL packet sent. Waiting for host to boot...")
            time.sleep(30)
            if is_host_reachable():
                print("Host is now online!")
            else:
                print("Host did not come online after WOL.")
        else:
            print("Failed to send WOL packet.")
