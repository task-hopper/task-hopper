#!/bin/bash


# TODO
# - probably set up pipenv and use that
# - add `hop upgrade` command to fetch latest version of hop
# - preserve existing hop config files
# - colorize output from install script
# - allow user to change install dir via command line argument
# - auto detect best shell rc file
# - allow user to change shell rc file via command line argument


INSTALL_DIR=\$HOME/.hop

SHELL_RC_FILE=$HOME/.bash_profile

REQUIRED_PYTHON_PACKAGES=("pyyaml" "jinja2")

# ensure python3 is installed
if [ ! -x "$(command -v python3)" ]; then
  echo "TaskHopper requires Python 3 to be installed."
  exit 1
fi

# ensure pip3 is installed
if [ ! -x "$(command -v pip3)" ]; then
  echo "TaskHopper requires Pip 3 to be installed."
  exit 1
fi

# install requirements
for req in "${REQUIRED_PYTHON_PACKAGES[@]}"; do
  echo "Installing $req..."
  pip3 install $req --disable-pip-version-check
done

# download task-hopper repo
curl --location --remote-header-name --remote-name https://github.com/task-hopper/task-hopper/archive/master.zip
unzip task-hopper-master.zip -d $INSTALL_DIR
rm -f task-hopper-master.zip

# add necessary environment variables / setup to user's shell configuration (.bashrc etc)
EXPORT_COMMAND="export HOP_DIR=\"$INSTALL_DIR\""
SOURCE_COMMAND="source \$HOP_DIR/hop/ext/hop.sh"

if grep -Fxq "$EXPORT_COMMAND" $SHELL_RC_FILE; then
  echo "\"$EXPORT_COMMAND\" already exists in $SHELL_RC_FILE"
else
  echo "Adding \"$EXPORT_COMMAND\" to $SHELL_RC_FILE"
  echo $EXPORT_COMMAND >> $SHELL_RC_FILE
fi

if grep -Fxq "$SOURCE_COMMAND" $SHELL_RC_FILE; then
  echo "\"$SOURCE_COMMAND\" already exists in $SHELL_RC_FILE"
else
  echo "Adding \"$SOURCE_COMMAND\" to $SHELL_RC_FILE"
  echo $SOURCE_COMMAND >> $SHELL_RC_FILE
fi

# TODO figure out why this shows the file as having a syntax error on mac
# source hop.sh to make hop immediately available in the current terminal session
source $HOP_DIR/hop/ext/hop.sh

echo "TaskHopper installation is complete! Run \`hop\` now to see available commands."
