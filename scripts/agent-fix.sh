#!/bin/bash
# agent-fix.sh - Automated fix assistant for Debian packaging build errors
#
# Reads build.log and applies targeted fixes to debian/ files.
# This script is a wrapper that outputs the build.log for AI agents
# to analyze and fix.

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_LOG="$PROJECT_ROOT/build.log"
DEBIAN_DIR="$PROJECT_ROOT/debian"

if [ ! -f "$BUILD_LOG" ]; then
    echo "ERROR: build.log not found at $BUILD_LOG"
    echo "Run scripts/build.sh first to generate build output."
    exit 1
fi

echo "=== Agent Fix ==="
echo "Analyzing: $BUILD_LOG"
echo ""

# Extract error summary
echo "--- Error Summary ---"
grep -E "error:|ERROR|dpkg-buildpackage: error|make: \*\*\*|scons: \*\*\*" "$BUILD_LOG" || echo "(no standard errors found)"

echo ""
echo "--- Last 50 lines ---"
tail -50 "$BUILD_LOG"

echo ""
echo "=== Fix Suggestions ==="
echo ""
echo "Common fixes:"
echo "  1. Missing Build-Depends -> edit debian/control"
echo "  2. SCons configuration -> edit debian/rules"
echo "  3. Patch failures -> edit debian/patches/ or series"
echo ""
echo "After fixing, re-run: ./scripts/build.sh"
