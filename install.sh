#!/usr/bin/env bash
set -e

VENV_DIR="$HOME/.hop/venv"
HOP_DIR="$HOME/.hop"
BIN_DIR="$HOME/.local/bin"
BIN_PATH="$BIN_DIR/hop"
WRAPPER_DEST="$HOP_DIR/hop.sh"

DEV=0
if [[ "${1:-}" == "--dev" ]]; then
    DEV=1
fi

echo "Installing task-hopper..."

mkdir -p "$HOP_DIR" "$BIN_DIR"

# Create isolated venv
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip

if [[ $DEV -eq 1 ]]; then
    REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "  Installing in dev (editable) mode from $REPO_DIR"
    "$VENV_DIR/bin/pip" install --quiet -e "$REPO_DIR"
    WRAPPER_SRC="$REPO_DIR/hop/ext/hop.sh.example"
else
    "$VENV_DIR/bin/pip" install --quiet task-hopper
    WRAPPER_SRC="$(echo "$VENV_DIR"/lib/python*/site-packages/hop/ext/hop.sh.example)"
fi

if [[ ! -f "$WRAPPER_SRC" ]]; then
    echo "ERROR: could not locate hop.sh.example at $WRAPPER_SRC" >&2
    exit 1
fi

# Write shim with hardcoded absolute path (safe against version managers intercepting 'hop')
cat > "$BIN_PATH" << EOF
#!/bin/bash
"$VENV_DIR/bin/hop" "\$@"
EOF
chmod +x "$BIN_PATH"
echo "  Shim written to $BIN_PATH"

# Write shell wrapper with hardcoded binary path (avoids command -v hop resolving to the shell function)
{ echo "HOP_BIN=\"$VENV_DIR/bin/hop\""; echo; cat "$WRAPPER_SRC"; } > "$WRAPPER_DEST"
echo "  Shell wrapper written to $WRAPPER_DEST"

# Inject shell integration into rc file (idempotent)
SHELL_NAME="$(basename "${SHELL:-}")"
case "$SHELL_NAME" in
    bash) RC_FILE="$HOME/.bashrc" ;;
    zsh)  RC_FILE="$HOME/.zshrc" ;;
    *)
        echo ""
        echo "  Unknown shell '$SHELL_NAME'. Add this to your shell config manually:"
        echo ""
        echo "    source $WRAPPER_DEST"
        echo ""
        RC_FILE=""
        ;;
esac

if [[ -n "$RC_FILE" ]]; then
    if grep -qF "source $WRAPPER_DEST" "$RC_FILE" 2>/dev/null; then
        echo "  Shell integration already present in $RC_FILE — skipping"
    else
        printf '\n# hop shell integration\nsource %s\n' "$WRAPPER_DEST" >> "$RC_FILE"
        echo "  Shell integration appended to $RC_FILE"
    fi
fi

# PATH check
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "  Note: $BIN_DIR is not on your PATH."
    echo "  Add this to your $RC_FILE (or equivalent):"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "Done. Reload your shell to start using hop:"
echo ""
echo "  source ${RC_FILE:-your shell config}"
echo ""
echo "Then run: hop -h"
