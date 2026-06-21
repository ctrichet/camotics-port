#!/bin/bash
set -e -o pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_DIR="$PROJECT_ROOT/upstream/camotics"
BUILD_DIR="$PROJECT_ROOT/build"
DISTRO="noble"

# Parse arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --distro)
      DISTRO="$2"
      shift 2
      ;;
    *)
      echo "Usage: $0 [--distro noble|bookworm]"
      echo "  --distro  Target distribution (default: noble)"
      exit 1
      ;;
  esac
done

echo "=== CAMotics Debian Package Build ==="
echo "Project root: $PROJECT_ROOT"
echo "Target distribution: $DISTRO"

# Prepare build directory
mkdir -p "$BUILD_DIR"
rm -rf "$BUILD_DIR/camotics"
cp -a "$UPSTREAM_DIR" "$BUILD_DIR/camotics"

# Copy Debian packaging into source tree
rm -rf "$BUILD_DIR/camotics/debian"
cp -a "$PROJECT_ROOT/debian" "$BUILD_DIR/camotics/debian"

# For non-default distro, adjust changelog so the target entry is at top
if [ "$DISTRO" = "bookworm" ]; then
  cd "$BUILD_DIR/camotics"
  # Remove the noble changelog entry from the build copy so bookworm becomes top
  # This only affects the build copy, not the original debian/changelog
  sed -i '/^camotics (1\.3\.0-1) noble;/,/^ --.*$/d' debian/changelog
  # Remove leading blank line left after noble entry removal
  sed -i '1{/^$/d}' debian/changelog
fi

# Build
cd "$BUILD_DIR/camotics"
dpkg-buildpackage -us -uc -b 2>&1 | tee "$PROJECT_ROOT/build.log"

echo "=== Build successful! ==="
echo "Packages:"
ls -la "$BUILD_DIR"/*.deb "$BUILD_DIR"/*.dsc 2>/dev/null
