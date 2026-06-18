#!/bin/bash
# Iterative build loop: retries build with agent fixes until success
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAX_RETRIES=${1:-10}

echo "=== Iterative Build Loop ==="
echo "Max retries: $MAX_RETRIES"

for i in $(seq 1 "$MAX_RETRIES"); do
    echo ""
    echo "=== Attempt $i/$MAX_RETRIES ==="

    if "$PROJECT_ROOT/scripts/build.sh"; then
        echo ""
        echo "=== Build succeeded on attempt $i! ==="
        exit 0
    fi

    echo "Build failed, invoking agent fix..."
    "$PROJECT_ROOT/scripts/agent-fix.sh"

    echo ""
    echo "Fix applied. Retrying..."
done

echo ""
echo "=== Build failed after $MAX_RETRIES attempts ==="
exit 1
