"""Check quest references, reachability, rewards and shipped localization."""
from pathlib import Path
from collections import Counter
import json
import re
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / 'tools/build_quests.py'), '--check'], check=True)
folder = root / 'pack/defaults/config/ftbquests/quests'
chapters = [json.loads(p.read_bytes().decode('utf-8')) for p in sorted((folder / 'chapters').glob('*.snbt'))]
quests = {q['id']: q for ch in chapters for q in ch['quests']}
assert len(chapters) == 7 and sum(len(c['quests']) for c in chapters) == len(quests) == 50
ids = []
for ch in chapters:
    ids.append(ch['id'])
    positions = set()
    for q in ch['quests']:
        assert re.search('[가-힣]', q['title']) and len(q['description']) >= 2
        assert (q['x'], q['y']) not in positions
        positions.add((q['x'], q['y']))
        ids.append(q['id'])
        assert set(q['dependencies']) <= quests.keys()
        assert q['id'] not in q['dependencies']
        assert q['tasks'] and q['rewards']
        for task in q['tasks']:
            ids.append(task['id'])
            assert task['type'] in {'item', 'checkmark'}
            if task['type'] == 'item':
                assert task['consume_items'] is False
                assert 1 <= task['count'] <= 64
        for reward in q['rewards']:
            ids.append(reward['id'])
            assert reward['type'] in {'xp', 'item'}, 'No privileged command or progression-skipping rewards'
            assert reward['team_reward'] is False
            if reward['type'] == 'xp':
                assert 1 <= reward['xp'] <= 75
            else:
                assert reward['item'].startswith('minecraft:') and 1 <= reward['count'] <= 4
assert len(ids) == len(set(ids)) and all(re.fullmatch('[0-7][0-9A-F]{15}', i) for i in ids)
done = set()
while True:
    ready = {i for i, q in quests.items() if set(q['dependencies']) <= done}
    if ready <= done:
        break
    done |= ready
assert done == quests.keys(), 'Quest graph contains a cycle or unreachable quest'
settings = json.loads((folder / 'data.snbt').read_text(encoding='utf-8'))
assert settings['version'] == 13 and settings['default_consume_items'] is False
assert settings['drop_loot_crates'] is False
ko_path = root / 'client-overrides/resourcepacks/FarmTech-Quests-Korean/assets/ftbquests/lang/ko_kr.json'
ko = json.loads(ko_path.read_bytes().decode('utf-8'))
jar = root / '.cache/downloads/mods/ftb-quests-forge-2001.4.22.jar'
if jar.exists():
    with zipfile.ZipFile(jar) as z:
        en = json.loads(z.read('assets/ftbquests/lang/en_us.json'))
    assert ko.keys() <= en.keys(), ko.keys() - en.keys()
    def formats(text):
        return Counter(re.findall(r'%(?:\d+\$)?([sd])', text))
    for key, translated in ko.items():
        assert translated and '\ufffd' not in translated
        assert formats(translated) == formats(en[key]), key
print(f'PASS: 50 reachable quests, stable unique IDs, bounded rewards, non-consuming tasks, {len(ko)} Korean UI entries')
