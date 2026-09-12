#!/usr/bin/env bash
set -Eeuo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
command -v docker >/dev/null
command -v flock >/dev/null
exec 9>.deploy.lock
flock -n 9 || { echo "Another FarmTech deployment is running." >&2; exit 1; }
if [[ ! -f .env ]]; then
    cp .env.example .env
    echo "Created .env. Read the Minecraft EULA and set EULA=true if you agree, then run bash deploy.sh again."
    exit 2
fi
docker compose config --quiet
if ! docker compose config --environment | grep -E '^EULA=(true|TRUE)$' >/dev/null; then
    echo "Read https://www.minecraft.net/eula and set EULA=true in .env if you agree." >&2
    exit 2
fi
mkdir -p data

# A failed download/build leaves the running server untouched.
docker compose build --pull minecraft
was_running=false
if docker compose ps --status running --services | grep -x minecraft >/dev/null; then
    was_running=true
fi
resume_on_error=false
on_error() {
    local status=$?
    if [[ "$resume_on_error" == true ]]; then
        echo "Pre-update backup failed; restarting the previous container." >&2
        docker compose start minecraft || true
    fi
    exit "$status"
}
trap on_error ERR
if [[ "$was_running" == true ]]; then
    docker compose stop --timeout 120 minecraft
    resume_on_error=true
fi
if [[ -f data/world/level.dat ]]; then
    mkdir -p deployment-backups
    stamp=$(date -u +%Y%m%dT%H%M%SZ)-$$
    paths=()
    for name in world config defaultconfigs tacz server.properties .farmtech-defaults eula.txt whitelist.json ops.json banned-players.json banned-ips.json; do
        [[ ! -e "data/$name" ]] || paths+=("$name")
    done
    tar -czf "deployment-backups/$stamp.tar.gz.part" -C data -- "${paths[@]}"
    mv "deployment-backups/$stamp.tar.gz.part" "deployment-backups/$stamp.tar.gz"
    echo "Pre-update backup: deployment-backups/$stamp.tar.gz"
fi
resume_on_error=false
docker compose up -d --no-build minecraft
docker compose logs --tail=40 minecraft
echo "Use docker compose logs -f to wait for the Minecraft Done message."
