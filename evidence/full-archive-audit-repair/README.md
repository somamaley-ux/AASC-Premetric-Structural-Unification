# Additive audit harness correction

The sealed package's original BundleInventory parser failed on the local name
`matches` after all 786 project sources and BundleEndpoint compiled. It produced
no successful full replay receipt. The original package and failed log remain
unchanged. This correction renames that local variable only; no mathematical
source or project import changes. This folder's manifest binds the corrected
audit, driver, original package manifest and prior failed audit log.

For a future complete fresh replay, inspect these sources, then run from this
folder using existing Python 3.11+:

```powershell
python -B -X utf8 replay.py --check
python -B -X utf8 -u replay.py --run --work-dir C:\short\new-replay --jobs 2
```

This supersedes the original package README's replay command. Keep `package/`
and `audit-repair/` as sibling folders. The driver copies and verifies the full
original package, builds all 786 project sources in an empty directory, then
compiles this corrected inventory against that fresh build. It preserves all
original package bytes. No installs, fetches or global configuration changes.

The actual retained audit uses `--resume-verified` once to revalidate every
original fresh source/object/direct-import/log receipt, additionally requiring
each object hash to equal its accepted predecessor. It then compiles the
corrected inventory and rechecks BundleEndpoint into new files. The final receipt
explicitly records both phases and the preserved initial parser failure.
The old failed log is historical failure evidence, excluded only from the new
successful audit's error gate, and is included in delivery. Every current
build/audit warning and every current error/panic remain subject to that gate.
