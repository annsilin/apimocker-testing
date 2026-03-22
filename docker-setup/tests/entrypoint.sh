#!/bin/bash

set -e

echo "[entrypoint] Running: pytest $*"
cd /app
exec pytest "$@"
