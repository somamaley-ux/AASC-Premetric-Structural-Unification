"""Read-only integrity checks for the repository export; does not invoke Lean."""
from pathlib import Path
import json,hashlib
from replay_composition import inspect_sources
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
paths={row['path'] for row in read('EXPORT_MANIFEST.json')['files']}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
        and not {'.git','.lake','__pycache__','build'}&set(p.relative_to(ROOT).parts)
        and p.name!='EXPORT_MANIFEST.json'}
assert actual==paths,('Export inventory differs',actual-paths,paths-actual)
assert sha(ROOT/'manifests/export-before-composition.json')=='255e4c9d13b5c107eb5edb9cfabc6224ba55a220f26dd0abc677f319fa49d8dd'
for row in read('composition/COPY_PROVENANCE.json')['copied_exactly']:
 assert sha(ROOT/row['repository_path'])==row['sha256'],row['repository_path']
meta=read('composition/EXPORT_BINDINGS.json')
rows,order,fields=inspect_sources(meta)
conclusions=read('composition/ROOT_CONCLUSIONS.json')
audit=read('composition/README_CLAIM_AUDIT.json')
assert conclusions['field_count']==49 and [r['field'] for r in conclusions['conclusions']]==fields
assert conclusions['source_sha256']==sha(ROOT/conclusions['source'])
assert audit['readme_sha256']==sha(ROOT/'README.md') and audit['root_source_sha256']==conclusions['source_sha256']
assert set(f for r in audit['claims'] for f in r['fields'])==set(fields)
assert not any(p.endswith(('.zip','.olean','.ilean')) for p in paths),'Binary replay artifacts must remain separate'
print(f'Verified {len(paths)+1} exported files, 839 baseline modules, 10 composition production modules and four audits.')
print('Verified 49 conclusion/proof assignments, copied evidence and README claim bindings; source bytes are unchanged.')
print('This integrity check does not invoke Lean or claim dependency/compiler bootstrap or empirical validation.')
