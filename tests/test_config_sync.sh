#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
source scripts/entrypoint.sh
sandbox=$(mktemp -d /tmp/farmtech-config-test.XXXXXX)
cleanup() { case "$sandbox" in /tmp/farmtech-config-test.*) rm -rf -- "$sandbox";; esac; }
trap cleanup EXIT
mkdir -p "$sandbox/seed/config" "$sandbox/data"
seed="$sandbox/seed"
data="$sandbox/data"
printf 'value=1\n' > "$seed/config/example.toml"
sync_defaults "$seed/" "$data/"
cmp "$seed/config/example.toml" "$data/config/example.toml"
printf 'value=2\n' > "$seed/config/example.toml"
sync_defaults "$seed" "$data"
grep -qx 'value=2' "$data/config/example.toml"
echo 'PASS: new and unchanged settings receive image defaults'

printf 'value=99\n' > "$data/config/example.toml"
sync_defaults "$seed" "$data"
grep -qx 'value=99' "$data/config/example.toml"
[[ ! -e "$data/config/example.toml.farmtech-new" ]]
printf 'value=3\n' > "$seed/config/example.toml"
sync_defaults "$seed" "$data"
grep -qx 'value=99' "$data/config/example.toml"
grep -qx 'value=3' "$data/config/example.toml.farmtech-new"
echo 'PASS: administrator changes survive and conflicts produce a review file'

mkdir -p "$sandbox/imported/config"
printf 'imported=keep\n' > "$sandbox/imported/config/example.toml"
sync_defaults "$seed" "$sandbox/imported"
grep -qx 'imported=keep' "$sandbox/imported/config/example.toml"
echo 'PASS: imported settings without a baseline are preserved'

mkdir -p "$sandbox/linked" "$sandbox/outside"
ln -s "$sandbox/outside" "$sandbox/linked/config"
if sync_defaults "$seed" "$sandbox/linked"; then
    echo 'FAIL: followed a configuration symlink' >&2; exit 1
fi
[[ ! -e "$sandbox/outside/example.toml" ]]
echo 'PASS: configuration sync does not follow external symlinks'

mkdir -p "$sandbox/image/mods" "$sandbox/links"
link_image_directory "$sandbox/links" "$sandbox/image" mods
[[ -L "$sandbox/links/mods" ]]
link_image_directory "$sandbox/links" "$sandbox/image" mods
mkdir -p "$sandbox/real/mods"
printf keep > "$sandbox/real/mods/custom.jar"
if link_image_directory "$sandbox/real" "$sandbox/image" mods; then
    echo 'FAIL: replaced a real mod directory' >&2; exit 1
fi
[[ -f "$sandbox/real/mods/custom.jar" ]]
echo 'PASS: image mod links are repeatable and preserve existing directories'

mkdir -p "$sandbox/eula-data"
if EULA=false DATA_DIR="$sandbox/eula-data" bash scripts/entrypoint.sh; then
    echo 'FAIL: accepted EULA implicitly' >&2; exit 1
else
    [[ $? -eq 2 ]]
fi
[[ -z "$(find "$sandbox/eula-data" -mindepth 1 -print -quit)" ]]
echo 'PASS: no EULA acceptance or data modification without administrator consent'
