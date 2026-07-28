#!/usr/bin/env bash
set -e

VENV_DIR="$HOME/.hop/venv"
BIN_DIR="$HOME/.local/bin"
BIN_PATH="$BIN_DIR/hop"

echo "Installing task-hopper..."

# Create isolated venv
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet task-hopper

# Write shim with hardcoded path to venv's hop binary
mkdir -p "$BIN_DIR"
cat > "$BIN_PATH" << EOF
#!/bin/bash
"$VENV_DIR/bin/hop" "\$@"
EOF
chmod +x "$BIN_PATH"

echo "Installed hop to $BIN_PATH"

# Check that $BIN_DIR is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "  Note: $BIN_DIR is not on your PATH."
    echo "  Add this to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "Next steps:"
echo "  1. Add the shell integration to your ~/.bashrc or ~/.zshrc:"
echo "       source /path/to/task-hopper/hop/ext/hop.sh.example"
echo "  2. Reload your shell: source ~/.bashrc"
echo "  3. Run: hop init"
