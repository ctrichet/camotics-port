#!/bin/bash
# Build CAMotics Debian package inside Debian Bookworm Docker container
set -e -o pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE="debian:bookworm"
CONTAINER_WORKDIR="/camotics-port"

echo "=== CAMotics Docker Build (Debian Bookworm) ==="
echo "Project root: $PROJECT_ROOT"
echo "Container image: $IMAGE"

# Check Docker availability
if ! docker info &>/dev/null; then
  echo "Error: Docker is not running. Check 'docker info'."
  exit 1
fi

# Ensure upstream source exists
if [ ! -d "$PROJECT_ROOT/upstream/camotics" ]; then
  echo "Error: upstream/camotics not found."
  echo "Run the CI clone steps first:"
  echo "  mkdir -p upstream"
  echo "  git clone --depth 1 https://github.com/CauldronDevelopmentLLC/CAMotics.git upstream/camotics"
  echo "  git clone --depth 1 https://github.com/CauldronDevelopmentLLC/cbang.git upstream/camotics/cbang"
  echo "  rm -rf upstream/camotics/.git upstream/camotics/cbang/.git"
  exit 1
fi

# Run build inside container
docker run --rm -i \
  -v "$PROJECT_ROOT:$CONTAINER_WORKDIR" \
  -w "$CONTAINER_WORKDIR" \
  "$IMAGE" \
  bash -c '
    set -e -o pipefail
    echo "=== Installing build dependencies ==="
    apt-get update -qq
    apt-get install -y -qq \
      scons python3-six build-essential debhelper desktop-file-utils \
      qtbase5-dev libqt5websockets5-dev \
      libglew-dev libcairo2-dev libdxflib-dev \
      libre2-dev libbz2-dev libsqlite3-dev \
      pkgconf libappstream-glib-dev lintian \
      libnode-dev

    echo "=== Building CAMotics for bookworm ==="
    ./scripts/build.sh --distro bookworm
  '

echo "=== Docker build complete! ==="
echo "Packages available at: $PROJECT_ROOT/build/"
ls -la "$PROJECT_ROOT/build/"*.deb 2>/dev/null
