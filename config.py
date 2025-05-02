# config.py

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

HOST_IP = os.getenv("HOST_IP")
HOST_MAC = os.getenv("HOST_MAC")
APP = os.getenv("APP")
LOG_FILE = os.getenv("LOG_FILE")

# Optional: Add checks to ensure required variables are set
required_vars = ["HOST_IP", "HOST_MAC", "APP", "LOG_FILE"]
for var in required_vars:
    if os.getenv(var) is None:
        print(f"Error: Required variable '{var}' not found in .env file.", file=sys.stderr)
        sys.exit(1)
