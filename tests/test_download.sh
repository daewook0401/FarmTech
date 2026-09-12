#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
sandbox=$(mktemp -d /tmp/farmtech-download-test.XXXXXX)
cleanup() { case "$sandbox" in /tmp/farmtech-download-test.*) rm -rf -- "$sandbox";; esac; }
trap cleanup EXIT
mkdir -p "$sandbox/bin"
cat > "$sandbox/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
while [[ $# -gt 0 ]]; do
    if [[ "$1" == --output ]]; then
        printf 'test artifact\n' > "$2"
        exit 0
    fi
    shift
done
exit 1
MOCK
chmod +x "$sandbox/bin/curl"
export PATH="$sandbox/bin:$PATH"
digest=$(printf 'test artifact\n' | sha256sum | cut -d ' ' -f 1)
printf '%s\tmods/test.jar\thttps://example.invalid/test.jar\n' "$digest" > "$sandbox/lock.tsv"
umask 077
bash tools/download.sh "$sandbox/lock.tsv" "$sandbox/downloads"
artifact="$sandbox/downloads/mods/test.jar"
[[ "$(stat -c %a "$artifact")" == 644 ]]
[[ "$(sha256sum "$artifact" | cut -d ' ' -f 1)" == "$digest" ]]
echo 'PASS: verified downloads are readable by the runtime account'
chmod 0600 "$artifact"
bash tools/download.sh "$sandbox/lock.tsv" "$sandbox/downloads"
[[ "$(stat -c %a "$artifact")" == 644 ]]
echo 'PASS: cached downloads also receive runtime read permission'
