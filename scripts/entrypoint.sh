#!/usr/bin/env bash
set -euo pipefail

sync_defaults() {
    local seed=$1 data=$2 source relative target baseline parent
    seed=$(cd "$seed" && pwd)
    data=$(cd "$data" && pwd)
    if [[ -L "$data/.farmtech-defaults" ]]; then
        echo "The baseline directory must not be a symlink." >&2
        return 1
    fi
    while IFS= read -r -d '' source; do
        relative=${source#"$seed"/}
        target="$data/$relative"
        baseline="$data/.farmtech-defaults/$relative"
        parent=$target
        while [[ "$parent" != "$data" ]]; do
            if [[ -L "$parent" ]]; then
                echo "Refusing to overwrite a configuration symlink: $parent" >&2
                return 1
            fi
            parent=$(dirname "$parent")
        done
        mkdir -p "$(dirname "$target")" "$(dirname "$baseline")"
        if [[ ! -e "$target" ]]; then
            cp "$source" "$target"
        elif cmp -s "$target" "$source"; then
            : # Already matches the image.
        elif [[ -f "$baseline" ]] && cmp -s "$target" "$baseline"; then
            cp "$source" "$target"
        elif [[ -f "$baseline" ]] && cmp -s "$source" "$baseline"; then
            : # Only the administrator changed the file.
        else
            if [[ -L "$target.farmtech-new" ]]; then
                echo "Refusing to overwrite a configuration symlink: $target.farmtech-new" >&2
                return 1
            fi
            cp "$source" "$target.farmtech-new"
            echo "Preserved local settings; review: $target.farmtech-new" >&2
        fi
        cp "$source" "$baseline"
    done < <(find "$seed" -type f -print0)
}

link_image_directory() {
    local data=$1 image=$2 name=$3 target="$1/$3"
    if [[ -L "$target" ]]; then
        if [[ "$(readlink "$target")" != "$image/$name" ]]; then
            echo "Unexpected symlink at $target; resolve it before updating." >&2
            return 1
        fi
    elif [[ -e "$target" ]]; then
        echo "$target already exists. Follow the README migration instructions; its files were preserved." >&2
        return 1
    else
        ln -s "$image/$name" "$target"
    fi
}

main() {
    local image=${PACK_DIR:-/opt/farmtech} data=${DATA_DIR:-/data}
    if [[ "${EULA,,}" != true ]]; then
        echo "Read https://www.minecraft.net/eula and set EULA=true in .env if you agree." >&2
        return 2
    fi
    local initial=${INIT_MEMORY:-2G} maximum=${MAX_MEMORY:-6G}
    if [[ ! "$initial" =~ ^[1-9][0-9]*[mMgG]$ || ! "$maximum" =~ ^[1-9][0-9]*[mMgG]$ ]]; then
        echo "INIT_MEMORY and MAX_MEMORY must look like 2G and 6G." >&2
        return 1
    fi
    if [[ ! -d "$data" || ! -w "$data" ]]; then
        echo "$data must be writable by the PUID:PGID configured in .env." >&2
        return 1
    fi
    link_image_directory "$data" "$image" mods
    link_image_directory "$data" "$image" libraries
    sync_defaults "$image/defaults" "$data"
    printf '# Accepted by the administrator through EULA=true in .env\neula=true\n' > "$data/eula.txt"
    mkdir -p "$data/backups" "$data/logs"
    cd "$data"
    exec java "-Xms$initial" "-Xmx$maximum" -Dfile.encoding=UTF-8 \
        @libraries/net/minecraftforge/forge/1.20.1-47.4.10/unix_args.txt nogui
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    EULA=${EULA:-false}
    main "$@"
fi
