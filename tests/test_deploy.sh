#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
source_repo=$PWD
sandbox=$(mktemp -d /tmp/farmtech-deploy-test.XXXXXX)
cleanup() { case "$sandbox" in /tmp/farmtech-deploy-test.*) rm -rf -- "$sandbox";; esac; }
trap cleanup EXIT
mkdir -p "$sandbox/bin"
cat > "$sandbox/bin/docker" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
echo "$*" >> "$MOCK_LOG"
case "$*" in
    'compose config --environment') echo 'EULA=true';;
    'compose build --pull minecraft') [[ "${FAIL_BUILD:-false}" != true ]] || exit 17;;
    'compose ps --status running --services') echo minecraft;;
esac
MOCK
chmod +x "$sandbox/bin/docker"
export PATH="$sandbox/bin:$PATH"
prepare() {
    local name=$1
    mkdir -p "$sandbox/$name/data/world"
    cp "$source_repo/deploy.sh" "$sandbox/$name/deploy.sh"
    printf 'EULA=true\n' > "$sandbox/$name/.env"
    printf 'mock world\n' > "$sandbox/$name/data/world/level.dat"
    export MOCK_LOG="$sandbox/$name/commands.log"
}
prepare success
bash "$sandbox/success/deploy.sh"
backup=$(find "$sandbox/success/deployment-backups" -name '*.tar.gz' -print -quit)
tar -tzf "$backup" | grep -x 'world/level.dat'
build_line=$(grep -n '^compose build' "$MOCK_LOG" | cut -d: -f1)
stop_line=$(grep -n '^compose stop' "$MOCK_LOG" | cut -d: -f1)
up_line=$(grep -n '^compose up' "$MOCK_LOG" | cut -d: -f1)
[[ "$build_line" -lt "$stop_line" && "$stop_line" -lt "$up_line" ]]
grep -qx 'mock world' "$sandbox/success/data/world/level.dat"
echo 'PASS: build precedes shutdown, a stopped-world backup precedes recreation'

prepare build-failure
if FAIL_BUILD=true bash "$sandbox/build-failure/deploy.sh"; then
    echo 'FAIL: build error was ignored' >&2; exit 1
else
    [[ $? -eq 17 ]]
fi
! grep -q '^compose stop' "$MOCK_LOG"
[[ ! -d "$sandbox/build-failure/deployment-backups" ]]
echo 'PASS: failed builds leave the running server alone'

prepare backup-failure
cat > "$sandbox/bin/tar" <<'MOCK'
#!/usr/bin/env bash
exit 23
MOCK
chmod +x "$sandbox/bin/tar"
if bash "$sandbox/backup-failure/deploy.sh"; then
    echo 'FAIL: backup error was ignored' >&2; exit 1
else
    [[ $? -eq 23 ]]
fi
grep -qx 'compose start minecraft' "$MOCK_LOG"
! grep -q '^compose up' "$MOCK_LOG"
grep -qx 'mock world' "$sandbox/backup-failure/data/world/level.dat"
echo 'PASS: failed backups resume the previous container without applying the new image'
