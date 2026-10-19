"""Private portable Windows replay; only bundled executables and ordinary file IO.

--check hashes the entire sealed package. --run copies it into a new directory,
rebuilds ALL project sources with bounded parallelism, then audits compiled terms.
Never fetches, installs, changes settings, deletes files, or runs archive scripts.
"""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, sys, time

def canonical(path):
    """One resolved extended-length spelling for all Windows containment checks."""
    text=os.path.abspath(os.fspath(path))
    def extended(s):
        if s.startswith('\\\\?\\UNC\\'): s='\\\\'+s[8:]
        elif s.startswith('\\\\?\\'): s=s[4:]
        s=os.path.normpath(s)
        return '\\\\?\\UNC\\'+s[2:] if s.startswith('\\\\') else '\\\\?\\'+s
    if os.name=='nt':
        return Path(extended(str(Path(extended(text)).resolve())))
    return Path(text).resolve()

REPAIR = canonical(Path(__file__).parent)
ROOT = canonical(REPAIR.parent/'package')

def check_repair():
    m=read(REPAIR/'manifest.json')
    assert sha(ROOT/'manifest.json')==m['package_manifest_sha256']
    expected={r['path']:r for r in m['files']}
    actual={p.relative_to(REPAIR).as_posix() for p in REPAIR.rglob('*') if p.is_file()}
    assert actual==set(expected)|{'manifest.json'}
    for rel,row in expected.items():
        p=safe(REPAIR,rel)
        assert not p.is_symlink() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    return m

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''): h.update(b)
    return h.hexdigest()

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def safe(root,rel):
    p=canonical(root/rel)
    assert p.is_relative_to(canonical(root)), ('escaping path',rel)
    return p

def check(root):
    manifest=read(root/'manifest.json')
    expected={r['path']:r for r in manifest['files']}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual==set(expected)|{'manifest.json'}, ('file set mismatch', sorted(actual-set(expected)-{'manifest.json'})[:10],sorted(set(expected)-actual)[:10])
    for idx,(rel,row) in enumerate(expected.items(),1):
        p=safe(root,rel)
        assert not p.is_symlink(), ('symlink',rel)
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], ('changed',rel)
        if idx%10000==0: print('VERIFIED',idx,'files',flush=True)
    print('PACKAGE_VERIFIED',len(expected),'files',sum(r['bytes'] for r in expected.values()),'bytes',flush=True)
    return manifest,expected

def resolve_object(module,roots):
    # Lean's namespace-root selection: select the first root with the root
    # namespace directory/file, then seek this module there. Do not fall through.
    first=module.split('.')[0]
    for root in roots:
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            p=root/(module.replace('.','/')+'.olean')
            assert p.is_file(), ('selected namespace lacks object',module,str(root))
            return p
    raise AssertionError(('no resolved object',module))

def run(work,jobs,resume=False):
    manifest,expected=check(ROOT)
    work=canonical(work)
    check_repair()
    assert not work.is_relative_to(ROOT) and not work.is_relative_to(REPAIR), 'Replay must be outside sealed inputs'
    started=time.time()
    if resume:
        assert work.is_dir() and not (work/'REPLAY_RECEIPT.json').exists()
    else:
        assert not work.exists(), 'Replay requires a new, nonexistent work directory'
        shutil.copytree(ROOT,work/'bundle')
    bundle=work/'bundle'; check(bundle)
    meta=read(bundle/'metadata/dependencies.json'); ledger=read(bundle/'metadata/project.json')
    sources={r['module']:r for r in ledger}; order=[r['module'] for r in ledger]
    lean=safe(bundle,meta['lean']); assert sha(lean)==meta['lean_sha256']
    build=work/'build'; build.mkdir(exist_ok=resume); logs=work/'logs'; logs.mkdir(exist_ok=resume)
    roots=[build]+[safe(bundle,r['root']) for r in meta['library_roots'] if not r.get('retained_path_missing')]
    env=os.environ.copy()
    for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LAKE','LAKE_HOME','ELAN_TOOLCHAIN']:
        env.pop(key,None)
    env['LEAN_PATH']=os.pathsep.join(map(str,roots))
    env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
    version=subprocess.run([str(lean),'--version'],env=env,capture_output=True,text=True,check=True).stdout.strip()
    lib=canonical(subprocess.run([str(lean),'--print-libdir'],env=env,capture_output=True,text=True,check=True).stdout.strip())
    assert lib.is_relative_to(bundle/'vendor/toolchain'), ('outside runtime',lib)
    roots.append(lib)
    receipts=[]; done=set(); pending=set(order); running={}; failed=None
    prior_failure=None; prior_endpoint=None
    if resume:
        files=list((work/'receipts').glob('*.json'))
        assert len(files)==len(order)==786
        saved={read(p)['module']:read(p) for p in files}
        assert set(saved)==set(sources)
        assert {p.relative_to(build).as_posix() for p in build.rglob('*.olean')}=={m.replace('.','/')+'.olean' for m in order}|{'BundleEndpoint.olean'}
        for m in order:
            r=saved[m]; row=sources[m]
            assert r['returncode']==0 and r['source']==row['source'] and r['source_sha256']==row['sha256']==sha(safe(bundle,row['source']))
            assert r['object']==str(Path('build')/(m.replace('.','/')+'.olean'))
            assert r['log']==str(Path('logs')/(m.replace('.','_')+'.log'))
            expected_command=[str(lean),'-j','2','-o',str(build/(m.replace('.','/')+'.olean')),str(safe(bundle,row['source']).relative_to(bundle/'src'))]
            assert r['command']==expected_command, ('prior compiler command mismatch',m)
            assert r['object_sha256']==sha(work/r['object'])==row['accepted_object_sha256']
            assert r['log_sha256']==sha(work/r['log'])
            assert [d['module'] for d in r['direct_imports']]==row['imports']
            for d in r['direct_imports']:
                obj=resolve_object(d['module'],roots)
                assert str(obj.relative_to(work))==d['object'] and sha(obj)==d['sha256']
                assert d['fresh_project_object']==(d['module'] in sources)
                if d['module'] in sources: assert obj==build/(d['module'].replace('.','/')+'.olean')
            receipts.append(r); done.add(m)
        pending.clear()
        failure=logs/'BundleInventory.log'
        assert sha(failure)==read(REPAIR/'manifest.json')['prior_failure_log_sha256']
        prior_failure={'log':str(failure.relative_to(work)),'sha256':sha(failure),
                       'kind':'audit harness parse failure before declaration scan',
                       'superseded_by':'logs/BundleInventoryRepaired.log'}
        prior_endpoint={'log':'logs/BundleEndpoint.log','log_sha256':sha(logs/'BundleEndpoint.log'),
                        'object':'build/BundleEndpoint.olean','object_sha256':sha(build/'BundleEndpoint.olean')}
        print('VERIFIED_PRIOR_FRESH_PROJECT_BUILD',len(done),'unchanged source/object/import/log receipts',flush=True)
    else:
        print('FRESH_PROJECT_BUILD',len(order),'modules',jobs,'workers',version,flush=True)
    def compile_one(module):
        row=sources[module]; src=safe(bundle,row['source']); assert sha(src)==row['sha256']
        obj=build/(module.replace('.','/')+'.olean'); obj.parent.mkdir(parents=True,exist_ok=True)
        direct=[]
        for imp in row['imports']:
            p=resolve_object(imp,roots)
            if imp in sources: assert p==build/(imp.replace('.','/')+'.olean'), ('cached project import',module,imp)
            direct.append({'module':imp,'object':str(p.relative_to(work)),'sha256':sha(p),
                           'fresh_project_object':imp in sources})
        log=logs/(module.replace('.','_')+'.log'); t=time.time()
        command=[str(lean),'-j','2','-o',str(obj),str(src.relative_to(bundle/'src'))]
        with log.open('wb') as out:
            p=subprocess.run(command,cwd=bundle/'src',env=env,stdout=out,stderr=subprocess.STDOUT)
        assert sha(src)==row['sha256'], ('source changed during compilation',module)
        for direct_row in direct:
            assert sha(work/direct_row['object'])==direct_row['sha256'], ('import changed during compilation',module,direct_row['module'])
        r={'module':module,'source':row['source'],'source_sha256':sha(src),
           'object':str(obj.relative_to(work)),'object_sha256':sha(obj) if obj.exists() else None,
           'returncode':p.returncode,'seconds':round(time.time()-t,3),
           'log':str(log.relative_to(work)),'log_sha256':sha(log),'command':command,'direct_imports':direct}
        write(work/'receipts'/(module.replace('.','_')+'.json'),r)
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        while pending or running:
            for m in order:
                if failed or len(running)>=jobs: break
                if m in pending and not (set(sources[m]['imports'])&set(sources)-done):
                    running[pool.submit(compile_one,m)]=m; pending.remove(m)
            if not running: break
            completed,_=concurrent.futures.wait(running,timeout=15,return_when=concurrent.futures.FIRST_COMPLETED)
            if not completed:
                print('BUILD_PROGRESS',len(done),'/',len(order),'active',','.join(running.values()),flush=True)
            for f in completed:
                m=running.pop(f)
                try: r=f.result()
                except BaseException as exc:
                    failed={'module':m,'exception':repr(exc)}; print('BUILD_EXCEPTION',failed,flush=True); continue
                receipts.append(r)
                if r['returncode']:
                    failed=r; print('BUILD_FAILED',m,r['log'],flush=True)
                else:
                    done.add(m); print('BUILT',len(done),'/',len(order),m,r['seconds'],'seconds',flush=True)
            if failed and not running: break
    base={'project_source_count':len(order),'fresh_project_objects':len(done),
          'dependency_binaries_rebuilt':False,'reused_dependencies':meta['library_roots'],
          'toolchain_sha256':sha(lean),'lean_version':version,
          'package_manifest_sha256':sha(ROOT/'manifest.json'),'search_roots':[str(p.relative_to(work)) for p in roots],
          'builds':receipts,'work_directory':str(work),'elapsed_seconds':round(time.time()-started,3)}
    if failed:
        write(work/'REPLAY_RECEIPT.json',dict(base,status='failed',failure=failed))
        raise SystemExit('Project build failed; inspect REPLAY_RECEIPT.json and preserved logs')
    assert len(done)==len(order)
    for name in ['BundleEndpoint','BundleInventory']:
        src=REPAIR/'BundleInventory.lean' if name=='BundleInventory' else bundle/'src'/(name+'.lean')
        suffix=('Repaired' if name=='BundleInventory' else 'Recheck') if resume else ''
        out=build/(name+suffix+'.olean'); log=logs/(name+suffix+'.log'); t=time.time()
        assert not out.exists() and not log.exists(), 'No audit output overwrites'
        print('CHECKING',name,flush=True)
        with log.open('wb') as f:
            p=subprocess.run([str(lean),'-j','2','-o',str(out),src.name],cwd=src.parent,env=env,stdout=f,stderr=subprocess.STDOUT)
        assert p.returncode==0, ('audit compilation failed',name,str(log))
        base[name]={'source_sha256':sha(src),'object_sha256':sha(out),'log_sha256':sha(log),'seconds':round(time.time()-t,3),'log':str(log.relative_to(work)),'object':str(out.relative_to(work))}
    lines=(work/base['BundleInventory']['log']).read_text(encoding='utf-8').splitlines()
    axioms=[json.loads(l.split('|',1)[1]) for l in lines if l.startswith('ROOT_AXIOMS|')]
    allowed={'Classical.choice','Quot.sound','propext'}
    expected_roots=read(bundle/'metadata/audit_roots.json')['loaded_roots']
    requested={(r['module'],r['name']) for r in expected_roots}
    actual=[]
    for r in axioms:
        matches=[pair for pair in requested if pair[0]==r['module'] and
                 (r['name']==pair[1] or r['name'].endswith('.'+pair[1]))]
        assert len(matches)==1, ('unexpected/ambiguous audited root',r)
        actual.append(matches[0])
    assert len(actual)==len(set(actual))==len(requested)==42 and set(actual)==requested
    assert all(set(r['axioms'])<=allowed for r in axioms)
    header=[json.loads(l.split('|',1)[1]) for l in lines if l.startswith('IMPORTED_MODULES|')]
    assert len(header)==1
    imports=[]
    for m in header[0]:
        p=resolve_object(m,roots)
        local=m in sources
        if local: assert p==build/(m.replace('.','/')+'.olean')
        else:
            rel=p.relative_to(bundle).as_posix()
            assert rel in expected and sha(p)==expected[rel]['sha256'], ('unsealed dependency',m)
        imports.append({'module':m,'path':str(p.relative_to(work)),'sha256':sha(p),'fresh_project_object':local})
    assert {r['module'] for r in imports if r['fresh_project_object']}==set(sources)
    count=[int(l.split('|')[1]) for l in lines if l.startswith('PROJECT_CONSTANT_COUNT|')]
    assert len(count)==1 and count[0]>=11603, ('unexpected declaration count',count)
    warnings=[]
    for p in logs.glob('*.log'):
        if prior_failure and str(p.relative_to(work))==prior_failure['log']: continue
        for i,l in enumerate(p.read_text(encoding='utf-8',errors='replace').splitlines(),1):
            if 'warning:' in l or 'error:' in l or 'panic' in l.lower(): warnings.append({'log':p.name,'line':i,'text':l})
    write(work/'EXACT_AXIOMS.json',axioms); write(work/'RESOLVED_IMPORTS.json',imports)
    errors=[r for r in warnings if 'error:' in r['text'] or 'panic' in r['text'].lower()]
    assert not errors, ('error/panic text in logs',errors)
    for r in receipts:
        assert sha(work/r['object'])==r['object_sha256'], ('project object changed after compilation',r['module'])
        assert sha(work/r['log'])==r['log_sha256'], ('project log changed',r['module'])
    check(bundle); check(ROOT); check_repair()
    base.update(audit_repair_manifest_sha256=sha(REPAIR/'manifest.json'),audit_repair_driver_sha256=sha(Path(__file__)),resumed_verified_project_build=resume,prior_failed_audit=prior_failure,prior_initial_endpoint=prior_endpoint,
                status='passed_with_warnings' if warnings else 'passed',compiled_project_declarations_inspected=count[0],exact_axiom_roots=axioms,
                imported_module_count=len(imports),resolved_imports_sha256=sha(work/'RESOLVED_IMPORTS.json'),
                warning_error_panic_lines=warnings,all_project_imports_fresh=True,
                dependency_rebuild_claim=False,elapsed_seconds=round(time.time()-started,3))
    write(work/'REPLAY_RECEIPT.json',base)
    print('REPLAY_PASSED',len(done),'fresh project objects',count[0],'compiled declarations',len(axioms),'exact roots',flush=True)
    print('RECEIPT',str(work/'REPLAY_RECEIPT.json'),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); p.add_argument('--run',action='store_true')
    p.add_argument('--resume-verified',action='store_true'); p.add_argument('--work-dir',type=Path); p.add_argument('--jobs',type=int,default=2); a=p.parse_args()
    assert a.jobs in {1,2,3,4}, 'Use 1-4 compiler workers'
    if a.run:
        assert a.work_dir, '--work-dir must name a new isolated directory'
        run(a.work_dir,a.jobs,a.resume_verified)
    elif a.check: check(ROOT); check_repair()
    else: p.print_help()
