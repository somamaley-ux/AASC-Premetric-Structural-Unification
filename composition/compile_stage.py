"""Compile only new successor sources against rehashed accepted dependencies."""
from pathlib import Path
import argparse,json,hashlib,os,subprocess,time,shutil
HERE=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
meta=read(HERE/'DEPENDENCIES.json')
def resolve(module):
    first=module.split('.')[0]
    for root in map(Path,meta['search_roots']):
        if (root/first).is_dir() or (root/(first+'.olean')).is_file():
            p=root/(module.replace('.','/')+'.olean')
            assert p.is_file(),('missing selected namespace object',module,p)
            return p
    raise AssertionError(('Unresolved import',module))
p=argparse.ArgumentParser();p.add_argument('module');p.add_argument('--revise-unsealed',action='store_true');args=p.parse_args()
module=args.module;assert module.isidentifier()
src=HERE/'src'/(module+'.lean');assert src.is_file()
if (HERE/'build'/(module+'.olean')).exists():
    assert args.revise_unsealed and not (HERE/'STAGE1_ACCEPTED.json').exists(),'Previously accepted stages are immutable'
    prior=read(HERE/'receipts'/(module+'.json'))
    assert sha(HERE/'build'/(module+'.olean'))==prior['object_sha256']
    assert sha(Path(prior['object']))==prior['object_sha256'] and sha(Path(prior['frozen_source']))==prior['source_sha256']
for row in meta['modules']:
    assert sha(HERE/row['source'])==row['source_sha256']
    assert sha(HERE/row['object'])==row['object_sha256']
for row in meta['prior_receipts']:assert sha(Path(row['path']))==row['sha256']
lean=Path(meta['lean']);assert sha(lean)==meta['lean_sha256']
parent=HERE/'attempts'/module;parent.mkdir(parents=True,exist_ok=True)
attempt=parent/(str(len(list(parent.iterdir()))+1).zfill(3));attempt.mkdir()
frozen=attempt/src.name;shutil.copyfile(src,frozen)
imports=[word for line in src.read_text(encoding='utf-8').splitlines() if line.startswith('import ') for word in line[7:].split()]
bindings=[{'module':m,'path':str(resolve(m)),'sha256':sha(resolve(m))} for m in imports]
env=os.environ.copy()
for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LAKE','LAKE_HOME','ELAN_TOOLCHAIN']:env.pop(key,None)
env['LEAN_PATH']=os.pathsep.join(meta['search_roots']);env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
obj=attempt/(module+'.olean');log=attempt/(module+'.log');cmd=[str(lean),'-j','2','-o',str(obj),src.name]
start=time.time()
with log.open('wb') as f:r=subprocess.run(cmd,cwd=src.parent,env=env,stdout=f,stderr=subprocess.STDOUT)
assert sha(src)==sha(frozen)
for row in bindings:assert sha(Path(row['path']))==row['sha256']
receipt={'module':module,'source':str(src),'source_sha256':sha(src),'frozen_source':str(frozen),
 'object':str(obj),'object_sha256':sha(obj) if obj.exists() else None,'log':str(log),'log_sha256':sha(log),
 'returncode':r.returncode,'seconds':round(time.time()-start,3),'command':cmd,'direct_imports':bindings,
 'dependency_objects_reused':True,'prior_receipts_unchanged':True}
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(log.read_text(encoding='utf-8',errors='replace'),end='')
if r.returncode==0:
    assert obj.exists()
    shutil.copyfile(obj,HERE/'build'/(module+'.olean'))
    shutil.copyfile(log,HERE/'logs'/(module+'.log'))
    (HERE/'receipts'/(module+'.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print('SUCCESSOR_BUILD',module,r.returncode,receipt['seconds'],'seconds',flush=True)
raise SystemExit(r.returncode)
