"""Recompile the new composition in a fresh directory; never replace originals.

Default: 10 new production modules plus the connected audit, using the 839
hash-verified previously accepted dependency objects. --full-local also rebuilds
the 839 local dependency sources. Neither mode bootstraps Lean/Mathlib binaries.
No downloads, installs, shell evaluation, corpus scripts, or deletes are used.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, time

HERE = Path(__file__).resolve().parent
PRODUCTION = ['KGOriginalMetricUseSemantics', 'KGCanonicalMetricLicensing',
 'KGLicensedEHReceiver', 'KGLicensedEHFailure', 'KGCanonicalScalarLicensing',
 'KGLicensedScalarReceiver', 'KGLicensedScalarEndpoint',
 'KGCommonLicensedPreparation', 'KGCommonLicensedEvolution',
 'KernelFaithfulLicensedEndpoints']

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''): h.update(block)
    return h.hexdigest()

def read(path): return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')

def imports(path):
    return [word for line in path.read_text(encoding='utf-8').splitlines()
        if line.startswith('import ') for word in line[7:].split()]

args = argparse.ArgumentParser()
args.add_argument('--output', default='replay-001')
args.add_argument('--full-local', action='store_true')
opt = args.parse_args()
out = (HERE / opt.output).resolve()
assert out.parent == HERE and out.name.startswith('replay-') and not out.exists(), out
meta = read(HERE/'DEPENDENCIES.json')
seal = read(HERE/'STAGE1_ACCEPTED.json')
pins = {Path(__file__).resolve(): sha(Path(__file__).resolve()),
  HERE/'DEPENDENCIES.json': sha(HERE/'DEPENDENCIES.json'),
  HERE/'STAGE1_ACCEPTED.json': sha(HERE/'STAGE1_ACCEPTED.json')}
for rel, expected in seal['files'].items(): assert sha(HERE/rel) == expected, rel
for row in meta['modules']:
    assert sha(HERE/row['source']) == row['source_sha256'], row['module']
    assert sha(HERE/row['object']) == row['object_sha256'], row['module']
for row in meta['prior_receipts']: assert sha(Path(row['path'])) == row['sha256']
lean = Path(meta['lean'])
assert sha(lean) == meta['lean_sha256']
pins[lean] = meta['lean_sha256']
new = PRODUCTION + ['Stage4ConnectedAudit']
expected = {}
for module in new:
    r = read(HERE/'receipts'/(module+'.json'))
    assert r['returncode'] == 0
    assert sha(HERE/'src'/(module+'.lean')) == r['source_sha256']
    assert sha(HERE/'build'/(module+'.olean')) == r['object_sha256']
    assert sha(Path(r['frozen_source'])) == r['source_sha256']
    assert sha(Path(r['object'])) == r['object_sha256']
    assert sha(Path(r['log'])) == r['log_sha256']
    assert sha(HERE/'logs'/(module+'.log')) == r['log_sha256']
    for path in [HERE/'receipts'/(module+'.json'), HERE/'src'/(module+'.lean'),
        HERE/'build'/(module+'.olean'), HERE/'logs'/(module+'.log'),
        Path(r['frozen_source']), Path(r['object']), Path(r['log'])]:
        pins[path] = sha(path)
    expected[module] = r
for row in meta['prior_receipts']: pins[Path(row['path'])] = row['sha256']

out.mkdir()
src = out/'src'; build = out/'build'; logs = out/'logs'; receipts = out/'receipts'
for path in [src, build, logs, receipts]: path.mkdir()
external = [Path(p) for p in meta['search_roots'][2:]]
roots = [build] + ([] if opt.full_local else [HERE/'cache']) + external
env = os.environ.copy()
for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LAKE','LAKE_HOME','ELAN_TOOLCHAIN']:
    env.pop(key, None)
env['LEAN_PATH'] = os.pathsep.join(map(str, roots))
env['PATH'] = str(lean.parent)+os.pathsep+env.get('PATH','')

rows = {r['module']: r for r in meta['modules']}
external_bindings = {}
external_modules = {dep for r in rows.values() for dep in r['imports'] if dep not in rows}
external_modules.update(dep['module'] for r in expected.values() for dep in r['direct_imports']
  if dep['module'] not in rows and dep['module'] not in expected)
for module in sorted(external_modules):
    first = module.split('.')[0]
    path = None
    for root in external:
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            path = root/(module.replace('.','/')+'.olean')
            assert path.is_file(), ('missing external namespace object', module, path)
            break
    assert path is not None, module
    external_bindings[module] = {'path': str(path), 'sha256': sha(path)}
    pins[path] = external_bindings[module]['sha256']
order = []
if opt.full_local:
    visited = set(); active = set()
    def visit(module):
        if module in visited: return
        assert module not in active, ('cyclic import', module)
        active.add(module)
        for dep in rows[module]['imports']:
            if dep in rows: visit(dep)
        active.remove(module); visited.add(module); order.append(module)
    for module in rows: visit(module)
order += new
for module in order:
    rel = Path(module.replace('.','/')+'.lean')
    original = HERE/rows[module]['source'] if module in rows else HERE/'src'/rel
    dst = src/rel; dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, dst)

def resolve(module):
    first = module.split('.')[0]
    for root in roots:
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            obj = root/(module.replace('.','/')+'.olean')
            assert obj.is_file(), ('missing selected namespace', module, obj)
            return obj
    raise AssertionError(('unresolved import', module))

baseline = {r['module']: r for r in meta['modules']}
fresh = set(order)
fresh_receipt_pins = {}
def binding_for(module, expected_old=None):
    path = resolve(module)
    if module in fresh:
        assert path == build/(module.replace('.','/')+'.olean')
    elif module in baseline:
        assert path == HERE/baseline[module]['object']
    elif expected_old is not None:
        assert path == Path(expected_old['path'])
    if module in external_bindings:
        assert path == Path(external_bindings[module]['path'])
    value = sha(path)
    if module in baseline:
        assert value == baseline[module]['object_sha256']
    elif module in expected:
        assert value == expected[module]['object_sha256']
    elif module in external_bindings:
        assert value == external_bindings[module]['sha256']
    else:
        raise AssertionError(('import absent from pinned old/fresh/external ledger', module))
    if expected_old is not None: assert value == expected_old['sha256']
    return {'module': module, 'path': str(path), 'sha256': value}

all_receipts = []
started = time.time()
for module in order:
    rel = Path(module.replace('.','/')+'.lean')
    source = src/rel; obj = build/rel.with_suffix('.olean')
    obj.parent.mkdir(parents=True, exist_ok=True)
    log = logs/(module+'.log')
    declared = imports(source)
    old_bindings = expected[module]['direct_imports'] if module in expected else None
    if old_bindings is not None: assert declared == [r['module'] for r in old_bindings]
    elif module in rows: assert declared == rows[module]['imports']
    bindings = [binding_for(dep, old_bindings[i] if old_bindings is not None else None)
      for i, dep in enumerate(declared)]
    cmd = [str(lean), '-j', '2', '-o', str(obj), str(rel)]
    start = time.time()
    with log.open('wb') as f:
        result = subprocess.run(cmd, cwd=src, env=env, stdout=f, stderr=subprocess.STDOUT)
    exp_source = rows[module]['source_sha256'] if module in rows else expected[module]['source_sha256']
    exp_object = rows[module]['object_sha256'] if module in rows else expected[module]['object_sha256']
    assert sha(source) == exp_source
    for binding in bindings: assert sha(Path(binding['path'])) == binding['sha256']
    receipt = {'module': module, 'returncode': result.returncode,
      'source_sha256': sha(source), 'object_sha256': sha(obj) if obj.exists() else None,
      'expected_object_sha256': exp_object, 'log_sha256': sha(log),
      'object_byte_identical': obj.exists() and sha(obj) == exp_object,
      'seconds': round(time.time()-start,3), 'command': cmd, 'direct_imports': bindings}
    output = log.read_text(encoding='utf-8', errors='replace')
    receipt['error_diagnostics'] = bool(re.search(
      r'(?im)(?:^.*:\s*error(?:\(|:)|PANIC|uncaught exception)', output))
    receipt['lint_warning_count'] = output.count(': warning:')
    if module in expected:
        prior_output = Path(expected[module]['log']).read_text(encoding='utf-8')
        receipt['expected_lint_warning_count'] = prior_output.count(': warning:')
        receipt['warnings_match_expected'] = receipt['lint_warning_count'] == receipt['expected_lint_warning_count']
    else:
        receipt['warnings_match_expected'] = True
    save(receipts/(module+'.json'), receipt)
    fresh_receipt_pins[receipts/(module+'.json')] = sha(receipts/(module+'.json'))
    all_receipts.append(receipt)
    print('CONNECTED_REPLAY', module, result.returncode, receipt['seconds'],
      receipt['object_byte_identical'], flush=True)
    if result.returncode != 0 or receipt['error_diagnostics'] or not receipt['object_byte_identical'] or not receipt['warnings_match_expected']:
        print(log.read_text(encoding='utf-8',errors='replace'), flush=True)
        save(out/'FAILED.json', {'failed': module, 'receipt': receipt})
        raise SystemExit(result.returncode or 1)

for rel, expected_hash in seal['files'].items(): assert sha(HERE/rel) == expected_hash, rel
for row in meta['modules']:
    assert sha(HERE/row['source']) == row['source_sha256']
    assert sha(HERE/row['object']) == row['object_sha256']
for path, value in pins.items(): assert sha(path) == value, ('changed pinned input', path)
for path, value in fresh_receipt_pins.items(): assert sha(path) == value, ('changed fresh receipt', path)
for receipt in all_receipts:
    module = receipt['module']; rel = Path(module.replace('.','/')+'.lean')
    assert sha(src/rel) == receipt['source_sha256']
    assert sha(build/rel.with_suffix('.olean')) == receipt['object_sha256']
    assert sha(logs/(module+'.log')) == receipt['log_sha256']
    for binding in receipt['direct_imports']:
        assert binding_for(binding['module']) == binding, ('changed import resolution', module, binding['module'])
warnings = sum(r['lint_warning_count'] for r in all_receipts)
save(out/'REPLAY_RECEIPT.json', {
 'status': 'passed_with_lint_warnings' if warnings else 'passed',
 'lint_warning_count': warnings, 'full_local_rebuild': opt.full_local,
 'new_production_modules': len(PRODUCTION), 'audit_modules': 1,
 'local_dependency_modules_rebuilt': len(rows) if opt.full_local else 0,
 'previously_accepted_dependency_objects_reused': 0 if opt.full_local else len(rows),
 'toolchain_and_library_binaries_reused': True, 'seconds': round(time.time()-started,3),
 'all_objects_byte_identical': all(r['object_byte_identical'] for r in all_receipts),
 'lean_sha256': meta['lean_sha256'], 'stage1_seal_sha256': sha(HERE/'STAGE1_ACCEPTED.json'),
 'dependency_manifest_sha256': sha(HERE/'DEPENDENCIES.json'),
 'replay_helper_sha256': pins[Path(__file__).resolve()],
 'external_direct_import_objects_pinned_and_rechecked': len(external_bindings),
 'all_fresh_triplets_receipts_original_inputs_and_import_bindings_rechecked': True,
 'all_baseline_sources_objects_and_stage1_seal_unchanged': True,
 'modules': all_receipts})
print('CONNECTED_REPLAY_PASSED', out/'REPLAY_RECEIPT.json', flush=True)
