#!/usr/bin/env bash

check_dependencies()
{
  # Python3
  if ! command -v python3 &>/dev/null
  then
    echo 'python3 must be installed'
  fi

  # Pip3
  if ! command -V pip3 &>/dev/null
  then
    echo 'pip3 must be installed'
  fi
}

check_dependencies
