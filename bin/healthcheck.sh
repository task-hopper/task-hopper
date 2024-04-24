#!/bin/bash


##############
# Variables  #
##############

# Colors
COLOR_RED="\033[1;31m"
COLOR_GREEN="\033[1;32m"
COLOR_RESET="\033[0m"

# Status
HEALTHCHECKS=()


#####################
# Utility Functions #
#####################

print_message() {
  if [ "${1:0:1}" = "✘" ]; then
    COLOR=${COLOR_RED}
  elif [ "${1:0:1}" = "✔" ]; then
    COLOR=${COLOR_GREEN}
  fi

  echo -e "${COLOR}${1}${COLOR_RESET}"
}

print_healthchecks() {
  if [ ! "$1" = "-s" ]; then
    echo "Task Hopper Health Check Results:"
    for CHECK in "${HEALTHCHECKS[@]}"; do
      print_message "${CHECK}"
    done
  fi
}


################
# Healthchecks #
################

# Assert python3 is installed
if command -v $HOP_PYTHON &>/dev/null; then
  HEALTHCHECKS+=("✔ Python 3 is installed")
else
  HEALTHCHECKS+=("✘ Python 3 is required but is not available.")
fi

# Assert python virtual environment exists
if [ ! -d "${HOP_VENV}" ] || [ ! -f "${HOP_VENV}/bin/activate" ]; then
  HEALTHCHECKS+=("✘ Python venv is missing or invalid")
  print_healthchecks "$1"
  exit 1
else
  HEALTHCHECKS+=("✔ Python venv is created and presumed valid")
  print_healthchecks "$1"
  exit 0
fi

# TODO Assert python dependencies are installed
