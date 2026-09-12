from pathlib import Path
import hashlib
import json
import re
import sys
import tomllib
import zipfile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'pack/manifest.json').read_text(encoding='utf-8'))
rows = {}
for name in ['mods.tsv', 'forge.tsv']:
    for line in (root / 'pack' / name).read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        digest, relative, url = line.split('\t')
        assert re.fullmatch(r'[0-9a-f]{64}', digest)
        assert relative == 'forge-installer.jar' or re.fullmatch(r'mods/[\w.+-]+\.jar', relative)
        assert url.startswith(('https://edge.forgecdn.net/', 'https://cdn.modrinth.com/', 'https://maven.minecraftforge.net/'))
        assert relative not in rows
        rows[relative] = (digest, url)
assert len(manifest['mods']) == 30
assert len(rows) == 31
for mod in manifest['mods']:
    assert rows['mods/' + mod['file']] == (mod['sha256'], mod['download_url'])
    assert not mod['file'].lower().startswith(('oculus-', 'embeddium-'))
assert rows['forge-installer.jar'] == (manifest['forge_installer']['sha256'], manifest['forge_installer']['download_url'])
for file in root.rglob('*'):
    if not file.is_file() or any(part in {'.git', '.cache', '__pycache__', 'data', 'deployment-backups'} for part in file.relative_to(root).parts):
        continue
    text = file.read_text(encoding='utf-8-sig')
    assert '\ufffd' not in text, str(file)
    if file.suffix == '.sh':
        assert b'\r' not in file.read_bytes(), str(file)
    if file.suffix == '.toml':
        tomllib.loads(text)
    if file.suffix == '.json':
        json.loads(text)
    assert not re.search(r'(?:[A-Z]:[\\/](?:Users|qk)[\\/]|/home/[a-z][\w-]+/|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})', text), str(file)
if len(sys.argv) > 1:
    cache = Path(sys.argv[1])
    for relative, (digest, _) in rows.items():
        file = cache / relative
        assert hashlib.sha256(file.read_bytes()).hexdigest() == digest, relative
        with zipfile.ZipFile(file) as archive:
            assert archive.testzip() is None, relative
print('PASS: manifest consistency, content versions, configuration syntax, portable text, and optional downloaded files')
