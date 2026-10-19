"""Read and hash originals; create only a new isolated verification receipt."""
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''): h.update(block)
    return h.hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))

output = HERE/'PRESERVATION_RECEIPT.json'
assert not output.exists()
meta = read(HERE/'DEPENDENCIES.json')
for row in meta['modules']:
    for path, expected in [(HERE/row['source'], row['source_sha256']),
        (HERE/row['object'], row['object_sha256']),
        (Path(row['original_source']), row['source_sha256']),
        (Path(row['original_object']), row['object_sha256'])]:
        assert sha(path) == expected, path
for rel, expected in read(HERE/'STAGE1_ACCEPTED.json')['files'].items():
    assert sha(HERE/rel) == expected, rel
for row in meta['prior_receipts']: assert sha(Path(row['path'])) == row['sha256']
public = Path('C:/Users/admin/Documents/Codex/2026-10-19/task/AASC-Premetric-Structural-Unification')
manifest = read(public/'EXPORT_MANIFEST.json')
for row in manifest['files']:
    path = public/row['path']
    assert path.is_file() and path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], path
result = {'status':'passed', 'baseline_modules':len(meta['modules']),
  'baseline_source_and_object_copies_and_originals_unchanged':True,
  'stage1_sealed_files_unchanged':True, 'prior_receipts_unchanged':True,
  'public_export_manifest_files_verified':len(manifest['files']),
  'public_export_manifest_sha256':sha(public/'EXPORT_MANIFEST.json'),
  'public_export_files_unchanged':True,
  'git_head_or_status_reverified':False,
  'git_qualification':'Content identity checked against the retained export manifest; no new Git command or repository mutation.'}
with output.open('x',encoding='utf-8') as f: json.dump(result,f,indent=2); f.write('\n')
print(json.dumps(result))
