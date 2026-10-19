"""Offline replay of the exported composition with explicitly supplied binaries.

--check-only needs only Python and repository files. Compilation requires the
exact pinned Lean executable, ordered external library roots and, by default,
the 839 accepted baseline objects. --full-local rebuilds those sources as well.
No downloads, installs, credential access, deletions or source changes occur.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,time

ROOT=Path(__file__).resolve().parents[1]
BINDINGS=ROOT/'composition/EXPORT_BINDINGS.json'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()

def read(path):return json.loads(path.read_text(encoding='utf8'))

def imports(path):
    return [word for line in path.read_text(encoding='utf8').splitlines()
            if line.startswith('import ') for word in line[7:].split()]

def source_path(row):
    path=(ROOT/row['source']).resolve()
    require(path.is_relative_to(ROOT),'Source escapes repository')
    return path

def inspect_sources(meta):
    baseline=meta['baseline']; production=meta['production']; audits=meta['audits']
    require((len(baseline),len(production),len(audits))==(839,10,4),'Module inventory changed')
    rows={r['module']:r for r in baseline+production+audits}
    require(len(rows)==853,'Duplicate module name')
    external={r['module']:r for r in meta['external_direct_imports']}
    require(len(external)==183,'External boundary changed')
    for row in rows.values():
        p=source_path(row)
        require(sha(p)==row['source_sha256'],'Source hash mismatch: '+row['module'])
        require(imports(p)==row['imports'],'Import mismatch: '+row['module'])
        for alias in row.get('equivalent_sources',[]):
            require(sha(ROOT/alias)==row['source_sha256'],'Shared source mismatch: '+alias)
        for dep in row['imports']:
            require(dep in rows or dep in external,'Unbound import: '+dep)
    # A topological pass checks the complete source union, including disconnected
    # accepted local modules, rather than only walking the final root imports.
    order=[];active=set();seen=set()
    def visit(module):
        if module in seen:return
        require(module not in active,'Cyclic imports: '+module)
        active.add(module)
        for dep in rows[module]['imports']:
            if dep in rows:visit(dep)
        active.remove(module);seen.add(module);order.append(module)
    for module in rows:visit(module)
    root_text=(ROOT/'composition/src/KernelFaithfulLicensedEndpoints.lean').read_text(encoding='utf8')
    declaration,proof=root_text.split('theorem kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger',1)
    fields=re.findall(r'^  (\w+)\s*:',declaration,re.M)
    assignments=re.findall(r'^  (\w+)[^\n]*:=',proof,re.M)
    require(len(fields)==49 and set(fields)==set(assignments),'Root fields/proof assignments changed')
    return rows,order,fields

def resolve(module,roots):
    first=module.split('.')[0]
    for root in roots:
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            obj=root/(module.replace('.','/')+'.olean')
            require(obj.is_file(),'Missing object in selected namespace: '+str(obj))
            return obj.resolve()
    raise RuntimeError('Unresolved import: '+module)

def save(path,data):
    with path.open('x',encoding='utf8',newline='\n') as f:
        json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true',help='Check public source hashes/imports/49-field proof without binaries or writes')
    parser.add_argument('--preflight',action='store_true',help='Also verify supplied compiler/cache/library identities; do not compile or write')
    parser.add_argument('--lean',type=Path)
    parser.add_argument('--library-root',type=Path,action='append',default=[],help='Repeat in the required Lean import-search order')
    parser.add_argument('--baseline-cache',type=Path,help='Root containing the 839 accepted module .olean files')
    parser.add_argument('--full-local',action='store_true',help='Rebuild all 839 local baseline sources; no compiler/library bootstrap')
    parser.add_argument('--output',type=Path,help='New, nonexistent directory for sources/build/logs/receipts')
    opt=parser.parse_args()
    meta=read(BINDINGS)
    rows,order,fields=inspect_sources(meta)
    if opt.check_only:
        print(json.dumps({'source_integrity':'passed','baseline_modules':839,'production_modules':10,'audit_modules':4,'root_conclusion_fields':len(fields),'external_import_names_bound':183,'lean_executed':False}))
        return
    require(opt.lean is not None and bool(opt.library_root),'Supply --lean and ordered --library-root arguments')
    lean=opt.lean.resolve(); libraries=[p.resolve() for p in opt.library_root]
    require(sha(lean)==meta['lean_sha256'],'Compiler hash differs from retained pinned runtime')
    require(opt.full_local or opt.baseline_cache is not None,'Supply --baseline-cache or request --full-local')
    cache=opt.baseline_cache.resolve() if opt.baseline_cache else None
    pinned={BINDINGS:sha(BINDINGS),Path(__file__).resolve():sha(Path(__file__).resolve()),lean:sha(lean)}
    for r in rows.values():
        pinned[source_path(r)]=r['source_sha256']
        for alias in r.get('equivalent_sources',[]):pinned[ROOT/alias]=r['source_sha256']
    if not opt.full_local:
        for row in meta['baseline']:
            p=cache/(row['module'].replace('.','/')+'.olean')
            require(sha(p)==row['object_sha256'],'Baseline object mismatch: '+row['module'])
            pinned[p]=row['object_sha256']
    external={r['module']:r for r in meta['external_direct_imports']}
    external_bindings={}
    for module,row in external.items():
        obj=resolve(module,libraries)
        require(sha(obj)==row['object_sha256'],'External object mismatch: '+module)
        pinned[obj]=row['object_sha256']
        external_bindings[module]={'module':module,'path':str(obj),'sha256':row['object_sha256']}
    if opt.preflight:
        print(json.dumps({'preflight':'passed','baseline_objects_verified':0 if opt.full_local else 839,'external_direct_import_objects_verified':len(external),'compiler_sha256':sha(lean),'lean_executed':False}))
        return
    require(opt.output is not None,'Supply --output for an actual replay')
    out=opt.output.resolve()
    require(not out.exists(),'Replay output already exists: '+str(out))
    require(not out.is_relative_to(ROOT/'composition/src'),'Output must not be inside sealed sources')
    selected=order if opt.full_local else [r['module'] for r in meta['production']+meta['audits']]
    fresh=set(selected)
    out.mkdir(parents=True)
    src=out/'src'; build=out/'build'; logs=out/'logs'; receipts=out/'receipts'
    for p in [src,build,logs,receipts]:p.mkdir()
    for module in selected:
        target=src/(module.replace('.','/')+'.lean');target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source_path(rows[module]),target)
    roots=[build]+([] if opt.full_local else [cache])+libraries
    env=os.environ.copy()
    for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LAKE','LAKE_HOME','ELAN_TOOLCHAIN']:env.pop(key,None)
    env['LEAN_PATH']=os.pathsep.join(map(str,roots));env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
    def binding(module):
        p=resolve(module,roots)
        if module in rows:
            expected=build/(module.replace('.','/')+'.olean') if module in fresh else cache/(module.replace('.','/')+'.olean')
            require(p==expected.resolve(),'Local import shadowing: '+module)
            expected_hash=rows[module]['object_sha256']
        else:
            require(str(p)==external_bindings[module]['path'],'External import shadowing: '+module)
            expected_hash=external[module]['object_sha256']
        require(sha(p)==expected_hash,'Import object identity mismatch: '+module)
        return {'module':module,'path':str(p),'sha256':expected_hash}
    all_receipts=[];started=time.time()
    try:
        for module in selected:
            row=rows[module];rel=Path(module.replace('.','/')+'.lean')
            source=src/rel;obj=build/rel.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
            log=logs/(module+'.log');bindings=[binding(m) for m in row['imports']]
            if 'direct_import_objects' in row:
                require([(b['module'],b['sha256']) for b in bindings]==[(b['module'],b['sha256']) for b in row['direct_import_objects']],'Retained direct import differs: '+module)
            cmd=[str(lean),'-j','2','-o',str(obj),str(rel)]
            then=time.time()
            with log.open('wb') as f:result=subprocess.run(cmd,cwd=src,env=env,stdout=f,stderr=subprocess.STDOUT)
            output=log.read_text(encoding='utf8',errors='replace')
            errors=bool(re.search(r'(?im)(?:^.*:\s*error(?:\(|:)|PANIC|uncaught exception)',output))
            warnings=output.count(': warning:')
            receipt={'module':module,'returncode':result.returncode,'source_sha256':sha(source),'object_sha256':sha(obj) if obj.is_file() else None,'expected_object_sha256':row['object_sha256'],'object_byte_identical':obj.is_file() and sha(obj)==row['object_sha256'],'log_sha256':sha(log),'lint_warning_count':warnings,'error_diagnostics':errors,'seconds':round(time.time()-then,3),'command':cmd,'direct_imports':bindings}
            save(receipts/(module+'.json'),receipt);all_receipts.append(receipt)
            require(result.returncode==0 and not errors,'Compiler/audit failed: '+module+'; see '+str(log))
            require(receipt['source_sha256']==row['source_sha256'],'Copied source changed: '+module)
            require(receipt['object_byte_identical'],'Compiled object differs from retained object: '+module)
            if 'warning_count' in row:require(warnings==row['warning_count'],'Warning count changed: '+module)
            for old in bindings:require(binding(old['module'])==old,'Import changed during compilation')
            print('COMPOSITION_REPLAY',module,'passed',receipt['seconds'],'seconds',flush=True)
        audit_totals={'declarations':0,'public_axiom_reports':0}
        for expected in meta['audit_expectations']:
            text=(logs/(expected['module']+'.log')).read_text(encoding='utf8')
            prefix=expected['prefix']
            require(f"{prefix}_CONSTANT_COUNT|{expected['declarations']}" in text,'Declaration count changed')
            require(f"{prefix}_PUBLIC_AUDIT_COUNT|{expected['public_axiom_reports']}" in text,'Public report count changed')
            reports=[json.loads(line.split('|',1)[1]) for line in text.splitlines() if line.startswith(prefix+'_DECLARATION|')]
            require(len(reports)==expected['public_axiom_reports'],'Audit report inventory differs')
            require(all(set(r['axioms'])<={'Classical.choice','Quot.sound','propext'} for r in reports),'Nonstandard axiom')
            audit_totals['declarations']+=expected['declarations'];audit_totals['public_axiom_reports']+=len(reports)
        connected=(logs/'Stage4ConnectedAudit.log').read_text(encoding='utf8')
        for name in meta['required_proof_dependencies']:require('CONNECTED_REQUIRED_PROOF_DEPENDENCY|'+name in connected,'Missing proof dependency: '+name)
        require('CONNECTED_PROOF_REACHABLE_CONSTANT_COUNT|66526' in connected,'Root proof traversal changed')
        for p,value in pinned.items():require(sha(p)==value,'Pinned input changed: '+str(p))
        for row in all_receipts:
            module=row['module'];rel=Path(module.replace('.','/')+'.lean')
            for p,key in [(src/rel,'source_sha256'),(build/rel.with_suffix('.olean'),'object_sha256'),(logs/(module+'.log'),'log_sha256')]:require(sha(p)==row[key],'Fresh output changed: '+str(p))
            require(read(receipts/(module+'.json'))==row,'Fresh receipt changed')
            for old in row['direct_imports']:require(binding(old['module'])==old,'Final import binding changed')
        report={'status':'passed_with_lint_warnings' if any(r['lint_warning_count'] for r in all_receipts) else 'passed','root':meta['root'],'root_conclusion_fields':49,'new_production_modules_rebuilt':10,'audit_modules_rebuilt':4,'baseline_modules_rebuilt':839 if opt.full_local else 0,'accepted_baseline_objects_reused':0 if opt.full_local else 839,'external_direct_import_objects_verified':183,'compiler_and_library_binaries_reused':True,'compiler_bootstrapped':False,'all_objects_byte_identical':all(r['object_byte_identical'] for r in all_receipts),'lint_warning_count':sum(r['lint_warning_count'] for r in all_receipts),'compiled_audit_totals':audit_totals,'root_proof_reachable_constants':66526,'binding_manifest_sha256':pinned[BINDINGS],'runner_sha256':pinned[Path(__file__).resolve()],'compiler_sha256':sha(lean),'full_local':opt.full_local,'seconds':round(time.time()-started,3),'search_roots':[str(p) for p in roots],'modules':all_receipts}
        save(out/'REPLAY_RECEIPT.json',report)
        print('COMPOSITION_REPLAY_PASSED',out/'REPLAY_RECEIPT.json',flush=True)
    except Exception as error:
        save(out/'FAILED.json',{'error':str(error),'completed_receipts':all_receipts})
        raise

if __name__=='__main__':main()
