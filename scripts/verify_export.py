"""Read-only integrity checks for the repository export; does not invoke Lean."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for row in read('EXPORT_MANIFEST.json')['files']:
 p=ROOT/row['path'];assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],row['path']
ledgers={}
for layer,count in [('dynamics',786),('licensing',64)]:
 rows=read('manifests/'+layer+'-sources.json');assert len(rows)==count
 ledgers[layer]={r['module']:r for r in rows}
 for r in rows:
  p=ROOT/r['path'];assert sha(p)==r['sha256'],r['path']
shared=set(ledgers['dynamics'])&set(ledgers['licensing'])
assert len(shared)==11
assert all(ledgers['dynamics'][m]['sha256']==ledgers['licensing'][m]['sha256'] for m in shared)
assert not list(ROOT.rglob('*.zip')), 'Full replay archive must remain separate'
print('Verified export manifest, 786 dynamics modules, 64 licensing modules and 11 shared source identities.')
print('No Lean compilation, dependency bootstrap, or empirical validation is asserted by this check.')
