#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
container=$(docker compose ps -q minecraft)
[[ -n "$container" ]] || { echo "The Minecraft container is not running." >&2; exit 1; }
echo "Type commands without /. Detach with Ctrl+P then Ctrl+Q."
exec docker attach --sig-proxy=false "$container"
