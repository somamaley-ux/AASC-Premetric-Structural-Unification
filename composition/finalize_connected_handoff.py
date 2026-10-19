"""Reconcile completed private evidence and write new, non-overwriting notes."""
from pathlib import Path
import hashlib, json, re

HERE = Path(__file__).resolve().parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(data,f,indent=2);f.write('\n')

notes=HERE/'FINAL_HANDOFF.md'; seal=HERE/'COMPOSITION_ACCEPTED.json'
assert not notes.exists() and not seal.exists()
reviews=['STAGE1_REVIEW.json','STAGE2_EH_REVIEW.json','STAGE3_SCALAR_REVIEW.json',
 'STAGE4_CONNECTED_REVIEW.json','REPLAY_REVIEW.json']
for name in reviews:
    review=read(HERE/name)
    assert review['outcome'].startswith('accepted'),name
    assert not review.get('blockers'),name
    for rel,expected in review.get('input_sha256',{}).items():
        assert sha(HERE/rel)==expected,(name,rel)

meta=read(HERE/'DEPENDENCIES.json')
for row in meta['modules']:
    for path,value in [(HERE/row['source'],row['source_sha256']),
        (HERE/row['object'],row['object_sha256']),
        (Path(row['original_source']),row['source_sha256']),
        (Path(row['original_object']),row['object_sha256'])]:
        assert sha(path)==value,path
for rel,value in read(HERE/'STAGE1_ACCEPTED.json')['files'].items():assert sha(HERE/rel)==value
for row in meta['prior_receipts']:assert sha(Path(row['path']))==row['sha256']
assert sha(Path(meta['lean']))==meta['lean_sha256']

roots=list(map(Path,meta['search_roots']))
def resolve(module):
    first=module.split('.')[0]
    for root in roots:
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            obj=root/(module.replace('.','/')+'.olean')
            assert obj.is_file(),obj
            return obj
    raise AssertionError(module)

builds=[]
for path in sorted((HERE/'receipts').glob('*.json')):
    row=read(path);module=row['module'];assert row['returncode']==0
    for path,value in [(Path(row['source']),row['source_sha256']),
        (Path(row['frozen_source']),row['source_sha256']),
        (Path(row['object']),row['object_sha256']),
        (Path(row['log']),row['log_sha256']),
        (HERE/'build'/(module+'.olean'),row['object_sha256']),
        (HERE/'logs'/(module+'.log'),row['log_sha256'])]:
        assert sha(path)==value,path
    for dep in row['direct_imports']:
        assert resolve(dep['module'])==Path(dep['path'])
        assert sha(resolve(dep['module']))==dep['sha256']
    builds.append(row)
assert len(builds)==14

counts=[('Stage1LicensingAudit','STAGE1',75,65),
 ('Stage2EHAudit','EH_ADAPTER',27,26),('Stage3ScalarAudit','SCALAR_LICENSE',80,70),
 ('Stage4ConnectedAudit','CONNECTED',70,69)]
for name,prefix,compiled,public in counts:
    log=(HERE/'logs'/(name+'.log')).read_text(encoding='utf-8')
    assert f'{prefix}_CONSTANT_COUNT|{compiled}' in log
    assert f'{prefix}_PUBLIC_AUDIT_COUNT|{public}' in log
replay=read(HERE/'replay-001/REPLAY_RECEIPT.json')
assert replay['status']=='passed_with_lint_warnings'
assert replay['new_production_modules']==10 and replay['audit_modules']==1
assert replay['lint_warning_count']==16 and replay['all_objects_byte_identical']
assert replay['previously_accepted_dependency_objects_reused']==839
assert not replay['full_local_rebuild']
assert replay['replay_helper_sha256']==sha(HERE/'replay_connected.py')
for row in replay['modules']:
    module=row['module'];assert row['returncode']==0 and row['object_byte_identical']
    assert read(HERE/'replay-001/receipts'/(module+'.json'))==row
    for folder,ext,key in [('src','.lean','source_sha256'),('build','.olean','object_sha256'),('logs','.log','log_sha256')]:
        assert sha(HERE/'replay-001'/folder/(module+ext))==row[key]

public=Path('C:/Users/admin/Documents/Codex/2026-10-19/task/AASC-Premetric-Structural-Unification')
for row in read(public/'EXPORT_MANIFEST.json')['files']:
    path=public/row['path'];assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256']
root='AASCKleinGordon.CanonicalLicensing.kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger'
text=f'''The private connected theorem is compiled, independently reviewed and replayed in its declared scope. The claim is derivation within the **Kernel and downstream Kernel-faithful machinery**, preserving the constraint-first dependency direction.

```lean
{root}
  (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
  KernelFaithfulLicensedEndpoints a s Ω
```

The [49-field proposition and proof](src/KernelFaithfulLicensedEndpoints.lean) contain actual canonical licenses, complete receiver maps, preservation and coverage, current EH and free-scalar analytic endpoints, and common original preparation/record/reference/evolution squares. Its fields are proved conclusions, with no desired endpoint certificate or unverified semantic bridge passed into the root. The common-source map covers the declared one-particle core with independently admitted metric operands. EH history continuation and scalar time evolution retain their distinct original meanings.

The [scope record](COMPOSITION_SCOPE.md) states every fixed construction choice and limitation. Positive mass/speed/ħ belong to `Parameters`; four spacetime and three spatial coordinates, the specific KG/free construction and original EH action are declared. EH receipts retain κ ≠ 0; arbitrary comparator equality retains the complete differential comparator class and dispersion calibration. The represented EH source is the action's geometric derivative. The theorem does not select a preferred metric, prove interface-order minimality, identify that source with independent matter, cover every Fock preparation or identify two complete physical interiors.

The import chain is concrete: `KernelFaithfulLicensedEndpoints` imports `KGCommonLicensedEvolution` and `KGLicensedScalarEndpoint`. The common-source branch imports `KGLicensedEHFailure` and `KGLicensedScalarReceiver`. Both receiving paths pass through `KGCanonicalMetricLicensing`; `KGOriginalMetricUseSemantics` imports the original EH source and `MetricityOriginalUseAssembly`. The scalar path also imports the actual NR receiving, exact-generator and calibrated-comparator constructions. Exact object paths/hashes are recorded in [build receipts](receipts) and [DEPENDENCIES.json](DEPENDENCIES.json).

All four substantive stages have independent acceptance: [original-use licensing](STAGE1_REVIEW.json), [EH adapter](STAGE2_EH_REVIEW.json), [scalar adapter](STAGE3_SCALAR_REVIEW.json), and [connected composition](STAGE4_CONNECTED_REVIEW.json). Their compiled audits cover 252 declarations, including generated/private declarations, and 230 exact public axiom reports. The policy rejects new axioms, opaque/unsafe declarations and sorry terms. The root depends only on `propext`, `Classical.choice` and `Quot.sound`. Its actual compiled proof-value closure reaches 66,526 constants and includes all seven required licensing/source/analytic/common-map dependencies.

The [fresh successor replay](replay-001/REPLAY_RECEIPT.json) rebuilt all ten new production modules and the connected audit from an empty successor build directory. All eleven objects are byte-identical to the reviewed originals. There are no errors; the sixteen reproduced warnings concern unused proof names in proposition fields. [Independent replay review](REPLAY_REVIEW.json) reconciles this evidence. This run reused 839 hash-verified, previously accepted local dependency objects and the pinned Lean/library binaries. It did not rebuild those 839 dependencies again or bootstrap the compiler/libraries. `replay_connected.py --full-local --output replay-full-001` provides an additional full-local source path; that mode has not been executed here.

The executed local reproduction command was:

```powershell
& 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python311\\python.exe' -B -X utf8 -u 'physical-work\\connected-canonical-licensing-20261019\\replay_connected.py'
```

That command uses this workspace's hash-bound dependency/runtime locations. The new composition has no separately verified portable runtime archive or public release. Reproduction in a different workspace needs a separately checked relocation/package step.

The original files remain intact: all 839 baseline copied/original source-object pairs, prior receipt pins, sealed Stage 1 files and all 902 public export manifest files were rechecked unchanged. No manuscript, public repository, system configuration or security setting was changed. Git HEAD/status was not freshly reverified; public content was compared with its retained export manifest.

The continuum-limit statement is specific: these receiving descriptions are constructed on declared continuum carriers, with no unproved discretization-to-continuum reconstruction. The separately proved KG nonrelativistic limit remains in the analytic chain. No universal continuum-limit or quantum-gravity solution follows.

The completed implementation phases are exact-edition/source freezing; concrete original-use tasks and positive safe regions; EH/scalar maps and common-source squares; and compiled audit, independent review and fresh successor replay. Further public release is outside this authorization. An expanded paper-level minimal-metric claim would require its exact projection order, class, source/role specialization and minimality obligations to be mechanized in that scope; necessity or an already reduced response cannot substitute for them.

The strongest bounded wording is:

> I have a machine-checked Lean 4 composition deriving the declared Einstein-form first-response and calibrated free-scalar Schrödinger endpoints within the Kernel and downstream Kernel-faithful machinery, through canonical licensing with proved receiver maps, stated coverage and common original-preparation records. This construction needs no discretization-to-continuum limit.

This composition is **private**. The earlier public source export discloses separate closures; it does not contain this theorem. The standalone Kernel release and its audit script are publicly listed, as recorded in the [supplementary link check](PUBLIC_LINK_RECHECK_20261019.md). Its archive listing is distinct from a freshly downloaded archive checksum and from a public release of the new composition. No public upload, push or DOI action was performed.
'''
notes.write_bytes(text.encode('utf-8'))
files={}
for folder in ['src','build','logs','receipts','replay-001/src','replay-001/build',
    'replay-001/logs','replay-001/receipts']:
    for path in sorted((HERE/folder).rglob('*')):
        if path.is_file():files[path.relative_to(HERE).as_posix()]=sha(path)
for name in reviews+['STAGE1_ACCEPTED.json','DEPENDENCIES.json','ROOT_FIELD_BINDINGS.json',
 'COMPOSITION_SCOPE.md','PUBLIC_LINK_RECHECK_20261019.md','FINAL_HANDOFF.md',
 'replay_connected.py','compile_stage.py','assemble_connected_root.py',
 'finalize_connected_handoff.py','verify_preservation.py','PRESERVATION_RECEIPT.json',
 'replay-001/REPLAY_RECEIPT.json']:
    files[name]=sha(HERE/name)
save(seal,{'status':'accepted_bounded_composition_private','root':root,
 'new_production_modules':10,'baseline_modules':839,'root_receipt_fields':49,
 'compiled_declarations':252,'official_public_axiom_reports':230,
 'axioms':['Classical.choice','Quot.sound','propext'],
 'fresh_replay_new_production_modules':10,'fresh_replay_audit_modules':1,
 'fresh_replay_all_objects_byte_identical':True,'lint_warnings':16,
 'full_local_839_rebuild_executed':False,'toolchain_library_bootstrap_executed':False,
 'originals_and_public_export_content_unchanged':True,'public_release_performed':False,
 'blockers_in_declared_bounded_scope':[],'files':files})
print('FINAL_PRIVATE_HANDOFF',notes)
print('FINAL_ACCEPTANCE_SHA256',sha(seal))
