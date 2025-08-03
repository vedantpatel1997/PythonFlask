#!/bin/bash

echo "========== [Startup Script Initiated] =========="

# Log current working directory and timestamp
echo "[INFO] Current Directory: $(pwd)"
echo "[INFO] Script Executed At: $(date)"

# Set custom virtual environment path
VENV_PATH="/home/site/wwwroot/vedantVirtualEnvironment/lib/python3.12/site-packages"
echo "[INFO] Setting PYTHONPATH to: $VENV_PATH"
export PYTHONPATH=$PYTHONPATH:"$VENV_PATH"

# Log Python version (to verify Azure compatibility)
echo "[INFO] Using Python Version:"
python3 --version

# Log installed packages (if needed for debugging)
echo "[INFO] Installed Python packages:"
python3 -m pip list

# Application startup
echo "[INFO] Launching Gunicorn with Uvicorn worker..."
echo "[INFO] Command: gunicorn -w 4 -b 0.0.0.0:8000 app:app"

# Start Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Log if execution falls through (shouldn't happen unless error occurs)
echo "[ERROR] Gunicorn process exited unexpectedly."

echo "========== [Startup Script Completed] =========="
