#!/bin/bash

# Wrapper script for GlassWorm Advanced Scanner

echo "GlassWorm Advanced Scanner"
echo "============================"
echo "This tool scans VS Code extensions for potential security threats."
echo ""

# Check if VS Code extensions directory exists
EXT_DIR="$HOME/.vscode/extensions"
if [ ! -d "$EXT_DIR" ]; then
    echo "Warning: VS Code extensions directory not found at $EXT_DIR"
    echo "Please install VS Code extensions first."
    exit 1
fi

echo "Found VS Code extensions directory."
echo ""

# Run the main scanner
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN_SCRIPT="$SCRIPT_DIR/glassworm-advanced.sh"

if [ ! -f "$SCAN_SCRIPT" ]; then
    echo "Error: Main scanner script not found at $SCAN_SCRIPT"
    exit 1
fi

echo "Running GlassWorm Advanced Scanner..."
echo ""

"$SCAN_SCRIPT"

echo ""
echo "Scan completed!"
echo "Reports are available in ~/glassworm-report/"
echo ""
echo "To view HTML report: firefox ~/glassworm-report/report.html"