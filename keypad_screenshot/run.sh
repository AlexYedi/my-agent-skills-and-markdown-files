#!/bin/bash
# Install dependencies and run the screenshot app

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install deps if needed
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# Run the app
python3 "$SCRIPT_DIR/screenshot_app.py"
