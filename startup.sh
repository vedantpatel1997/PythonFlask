#!/bin/bash

#=============================#
#      Custom Startup Log     #
#=============================#

# Define color-coded log prefixes
INFO="\033[1;34m[INFO]\033[0m"
WARN="\033[1;33m[WARN]\033[0m"
ERROR="\033[1;31m[ERROR]\033[0m"
SUCCESS="\033[1;32m[SUCCESS]\033[0m"
SECTION="\033[1;35m====>\033[0m"

echo -e "$SECTION \033[1mStartup Script Initiated\033[0m"
echo -e "$INFO Timestamp       : $(date)"
echo -e "$INFO Hostname        : $(hostname)"
echo -e "$INFO Working Dir     : $(pwd)"
echo -e "$INFO User            : $(whoami)"

#=============================#
#   Set and Verify VENV PATH  #
#=============================#

VENV_PATH="/home/site/wwwroot/vedantVirtualEnvironment/lib/python3.12/site-packages"
echo -e "$INFO Configuring PYTHONPATH..."
export PYTHONPATH="$PYTHONPATH:$VENV_PATH"
echo -e "$SUCCESS PYTHONPATH set to: $PYTHONPATH"

#=============================#
#     Python Environment      #
#=============================#

echo -e "$INFO Verifying Python installation..."
if command -v python3 &>/dev/null; then
    echo -e "$SUCCESS Python Version  : $(python3 --version)"
else
    echo -e "$ERROR Python3 not found in path!"
    exit 1
fi

echo -e "$INFO Listing installed packages..."
python3 -m pip list || echo -e "$WARN Could not list Python packages."

#=============================#
#     Gunicorn Execution      #
#=============================#

APP_MODULE="app:app"
BIND_ADDRESS="0.0.0.0:8000"
WORKERS=4

echo -e "$INFO Starting Gunicorn server..."
echo -e "$INFO Command: gunicorn -w $WORKERS -b $BIND_ADDRESS $APP_MODULE"

gunicorn --worker-class uvicorn.workers.UvicornWorker \
         -w $WORKERS \
         -b $BIND_ADDRESS \
         $APP_MODULE

GUNICORN_EXIT_CODE=$?

#=============================#
#       Final Logging         #
#=============================#

if [[ $GUNICORN_EXIT_CODE -ne 0 ]]; then
    echo -e "$ERROR Gunicorn exited with code: $GUNICORN_EXIT_CODE"
else
    echo -e "$SUCCESS Gunicorn exited normally."
fi

echo -e "$SECTION \033[1mStartup Script Completed\033[0m"
