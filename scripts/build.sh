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
      echo "Usage: $0 [--distro noble|bookworm|resolute]"
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

# Adjust changelog so only the target distro entry remains at top
# This only affects the build copy, not the original debian/changelog
cd "$BUILD_DIR/camotics"
for d in $(sed -n 's/^camotics (1\.[0-9.]\+-[0-9]\+) \([^;]*\);.*/\1/p' debian/changelog); do
  if [ "$d" != "$DISTRO" ]; then
    sed -i "/^camotics (1\.[0-9.]\+-[0-9]\+) $d;/,/^ --.*$/d" debian/changelog
  fi
done
sed -i '1{/^$/d}' debian/changelog

# Build
cd "$BUILD_DIR/camotics"
dpkg-buildpackage -us -uc -b 2>&1 | tee "$PROJECT_ROOT/build.log"

echo "=== Build successful! ==="
echo "Packages:"
ls -la "$BUILD_DIR"/*.deb 2>/dev/null || true
