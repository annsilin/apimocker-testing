#!/bin/bash
# Фиксируем права на docker socket при каждом старте,
# чтобы jenkins мог запускать docker run без sudo.
chmod 666 /var/run/docker.sock 2>/dev/null || true

exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
