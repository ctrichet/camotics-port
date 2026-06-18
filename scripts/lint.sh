#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEBIAN_DIR="$PROJECT_ROOT/debian"

echo "=== Debian packaging lint ==="
ERRORS=0

# Check required files
for f in control rules changelog copyright compat; do
    if [ ! -f "$DEBIAN_DIR/$f" ]; then
        echo "ERROR: Missing $DEBIAN_DIR/$f"
        ERRORS=$((ERRORS + 1))
    else
        echo "  OK: $f"
    fi
done

# Check debian/source/format
if [ ! -f "$DEBIAN_DIR/source/format" ]; then
    echo "ERROR: Missing debian/source/format"
    ERRORS=$((ERRORS + 1))
else
    echo "  OK: source/format"
fi

# Check rules is executable
if [ -f "$DEBIAN_DIR/rules" ] && [ ! -x "$DEBIAN_DIR/rules" ]; then
    echo "ERROR: debian/rules is not executable"
    ERRORS=$((ERRORS + 1))
elif [ -f "$DEBIAN_DIR/rules" ]; then
    echo "  OK: rules is executable"
fi

# Check patches/series
if [ -d "$DEBIAN_DIR/patches" ] && [ ! -f "$DEBIAN_DIR/patches/series" ]; then
    echo "WARNING: debian/patches/ exists but no series file"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "All checks passed!"
else
    echo "$ERRORS error(s) found."
    exit 1
fi
