#!/bin/bash
set -e -o pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_DIR="$PROJECT_ROOT/upstream/camotics"
BUILD_DIR="$PROJECT_ROOT/build"

echo "=== CAMotics Debian Package Build ==="
echo "Project root: $PROJECT_ROOT"

# Prepare build directory
mkdir -p "$BUILD_DIR"
rm -rf "$BUILD_DIR/camotics"
cp -a "$UPSTREAM_DIR" "$BUILD_DIR/camotics"

# Copy Debian packaging into source tree
rm -rf "$BUILD_DIR/camotics/debian"
cp -a "$PROJECT_ROOT/debian" "$BUILD_DIR/camotics/debian"

# Build
cd "$BUILD_DIR/camotics"
dpkg-buildpackage -us -uc 2>&1 | tee "$PROJECT_ROOT/build.log"

echo "=== Build successful! ==="
echo "Packages:"
ls -la "$BUILD_DIR"/*.deb "$BUILD_DIR"/*.dsc 2>/dev/null
