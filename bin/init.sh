#!/bin/bash

#############
# Variables #
#############
# Colors
RED="\033[1;31m"
GREEN="\033[1;32m"
COLOR_RESET="\033[0m"

# Python
if [ -n "$HOP_SYS_PY" ]; then
  HOP_PY=$HOP_SYS_PY
else
  HOP_PY=/usr/bin/python3
fi


initialize_hop() {
  # 1. Check that python 3 is available
  if ! command -v $HOP_PY &>/dev/null; then
    echo -e "${RED}✘ Python 3 is required but is not available.${COLOR_RESET}"
    exit 1
  else
    echo 'Initializing task-hopper...'
  fi

  # 2. delete existing venv if it exists
  if [ ! d "${HOP_VENV}" ]; then
    echo 'Removing previous virtual environment...'
    rm -r $HOP_VENV &>/dev/null
  fi


  # 3. Create a new virtual environment
  echo 'Setting up new virtual environment...'
  $HOP_PY -m venv $HOP_VENV

  # 4. Install Python dependencies from requirements.txt
  echo 'Installing python dependencies...'
  $HOP_VENV/bin/pip install -r "${HOP_REPO}/requirements.txt"
}

~/repos/personal/task-hopper-two/bin/healthcheck.sh -s
HEALTHCHECK_STATUS="$?"

if [ "$HEALTHCHECK_STATUS" -eq 1 ] || [ "$1" = "-f" ]; then
  initialize_hop
  echo '...Initialize complete'
else
  echo 'task-hopper has already initialized'
fi

