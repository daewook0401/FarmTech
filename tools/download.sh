#!/usr/bin/env bash
set -euo pipefail
lock_file=${1:?Usage: download.sh LOCK_FILE OUTPUT_DIRECTORY}
output=${2:?Usage: download.sh LOCK_FILE OUTPUT_DIRECTORY}
mkdir -p "$output"
output=$(cd "$output" && pwd)
temporary=
trap 'if [[ -n "$temporary" && -f "$temporary" ]]; then rm -f -- "$temporary"; fi' EXIT

while IFS=$'\t' read -r digest relative url extra || [[ -n "${digest:-}" ]]; do
    [[ -z "$digest" || "$digest" == \#* ]] && continue
    if [[ ! "$digest" =~ ^[a-f0-9]{64}$ || -n "${extra:-}" ]]; then
        echo "Invalid checksum row in $lock_file" >&2
        exit 1
    fi
    if [[ ! "$relative" =~ ^mods/[a-zA-Z0-9_.+-]+\.jar$ && "$relative" != forge-installer.jar ]]; then
        echo "Invalid download path: $relative" >&2
        exit 1
    fi
    [[ "$url" == https://* ]] || { echo "HTTPS download required" >&2; exit 1; }
    target="$output/$relative"
    mkdir -p "$(dirname "$target")"
    if [[ -f "$target" ]] && [[ "$(sha256sum "$target" | cut -d ' ' -f 1)" == "$digest" ]]; then
        echo "Verified cache: $relative"
        continue
    fi
    temporary=$(mktemp "$target.part.XXXXXX")
    echo "Downloading: $relative"
    curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
        --retry 3 --connect-timeout 20 --max-time 300 --output "$temporary" "$url"
    actual=$(sha256sum "$temporary" | cut -d ' ' -f 1)
    if [[ "$actual" != "$digest" ]]; then
        echo "SHA-256 mismatch for $relative: expected $digest, received $actual" >&2
        exit 1
    fi
    mv -f -- "$temporary" "$target"
    temporary=
done < "$lock_file"
