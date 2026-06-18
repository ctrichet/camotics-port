#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"

echo "=== Lintian check ==="

DEB_FILE=$(ls "$BUILD_DIR"/*.deb 2>/dev/null | head -1)
if [ -z "$DEB_FILE" ]; then
    echo "ERROR: No .deb file found in $BUILD_DIR"
    echo "Run scripts/build.sh first."
    exit 1
fi

echo "Checking: $DEB_FILE"
lintian --info --display-experimental "$DEB_FILE" 2>&1
echo "=== Lintian check complete ==="
